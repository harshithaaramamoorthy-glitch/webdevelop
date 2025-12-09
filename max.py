import random
from fastapi import FastAPI
app= FastAPI()
@app.get("/")
def home():
    return{"message":"welcome to the Randomizer API"}
@app.get("/random/{max_value}")
def get_random_number(max_value:int):
    return{
        "max": max_value,
        "random_number":random.randit(1,max_value)
    }