from fastapi import FastAPI,HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")

client=AsyncIOMotorClient(MONGO_URI)
db=client["genaiproject"]
euroon_data=db["api_project"]

app = FastAPI()

class eurondata(BaseModel):
    name: str
    age: int
    city: str
    course: str

@app.post("/euron/insert")
async def euron_data_insert_helper(data:eurondata):
    result = await euroon_data.insert_one(data.model_dump())
    return {"message":"Data inserted successfully", "id": str(result.inserted_id)}

def euron_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@app.get("/euron/data")
async def get_euron_data():
    iterms = []
    cursor = euroon_data.find({})
    async for document in cursor:
        iterms.append(euron_helper(document))
    return iterms

