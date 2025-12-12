import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# -------------------------------
# Database configurations (MySQL)
# -------------------------------
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:harshithaa%4099@localhost:3306/employeedb"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -------------------------------
# SQLAlchemy models
# -------------------------------
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# -------------------------------
# FastAPI app instance + templates/static
# -------------------------------
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Optional: serve static files (CSS/js). Create a "static" folder if you want.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# Routes (server-rendered HTML)
# -------------------------------

@app.get("/", response_class=HTMLResponse)
def read_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(Item).order_by(Item.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


@app.get("/items/{item_id}", response_class=HTMLResponse)
def read_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("detail.html", {"request": request, "item": item})


@app.get("/create", response_class=HTMLResponse)
def create_item_form(request: Request):
    # show empty form
    return templates.TemplateResponse("form.html", {"request": request, "action": "/create", "item": None})


@app.post("/create")
def create_item_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # Redirect to list (Post-Redirect-Get)
    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{item_id}", response_class=HTMLResponse)
def edit_item_form(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("form.html", {"request": request, "action": f"/edit/{item_id}", "item": item})


@app.post("/edit/{item_id}")
def edit_item_post(
    request: Request,
    item_id: int,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = name
    db_item.description = description
    db.commit()
    db.refresh(db_item)
    return RedirectResponse(url=f"/items/{item_id}", status_code=303)


@app.post("/delete/{item_id}")
def delete_item_post(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


# -------------------------------
# Run FastAPI app
# -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
