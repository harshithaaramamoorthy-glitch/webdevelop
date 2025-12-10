from fastapi import APIRouter
router = APIRouter()
@router.get("/permission")
async def get_all_permission():
 return {"message": "List of permission"}



