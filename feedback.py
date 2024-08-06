from fastapi import APIRouter, HTTPException, status
from pymongo import MongoClient
from bson import ObjectId
from feedbackmodel import FeedbackModel
import logging
import os
from dotenv import load_dotenv

load_dotenv()
# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# MongoDB connection setup

try:
    client = MongoClient(os.environ["MONGODB_URI"])
    db = client["Application"]
    feedback_collection = db["feedbacks"]
    logger.info("MongoDB connection established successfully.")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise

@router.post("/add-feedback/", response_model=FeedbackModel)
async def add_feedback(feedback: FeedbackModel):
    try:
        feedback_data = feedback.dict()
        feedback_data["_id"] = ObjectId()
        feedback_collection.insert_one(feedback_data)
        logger.debug(f"Inserted feedback: {feedback_data}")
        return feedback_data
    except Exception as e:
        logger.error(f"Error adding feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get-feedback/{feedback_id}", response_model=FeedbackModel)
async def get_feedback(feedback_id: str):
    try:
        feedback = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
        if feedback is None:
            logger.warning(f"Feedback with ID {feedback_id} not found.")
            raise HTTPException(status_code=404, detail="Feedback not found")
        logger.debug(f"Retrieved feedback: {feedback}")
        return feedback
    except Exception as e:
        logger.error(f"Error retrieving feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
