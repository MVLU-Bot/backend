from fastapi import APIRouter, HTTPException, Request
from pymongo import MongoClient
from bson import ObjectId
from feedbackmodel import FeedbackModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# MongoDB connection setup
client = MongoClient("mongodb+srv://sahilsinghmongotest:sahilsingh72@cluster0.xw4zw.mongodb.net/")
db = client["feedback_database"]
feedback_collection = db["feedbacks"]

def get_client_ip(request: Request) -> str:
    # Extract the client IP address from the request
    if "x-forwarded-for" in request.headers:
        ip = request.headers["x-forwarded-for"].split(",")[0]
    else:
        ip = request.client.host
    return ip

@router.post("/add-feedback/", response_model=FeedbackModel)
async def add_feedback(feedback: FeedbackModel, request: Request):
    feedback_data = feedback.dict()
    feedback_data["_id"] = ObjectId()
    feedback_data["context"] = get_client_ip(request)
    feedback_collection.insert_one(feedback_data)
    return feedback_data

@router.get("/get-feedback/{feedback_id}", response_model=FeedbackModel)
async def get_feedback(feedback_id: str):
    feedback = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback
