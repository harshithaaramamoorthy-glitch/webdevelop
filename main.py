from fastapi import FastAPI
app = FastAPI() #help to install supporting files
@app.get("/")
def read_root():
    return {"Hello": "World"}