from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, UTC
import os

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection
mongo_uri = os.getenv("DB_URI")
client = MongoClient(mongo_uri)
db = client["HR-Automation-form-data"]
collection = db["form-submission-data"]

# Pydantic model for form response
class FormResponse(BaseModel):
    responseId: str
    submitter: str
    responses: dict

# API endpoint to save form response
@app.post("/api/form-responses")
async def save_form_response(response: FormResponse):
    try:
        # Prepare document for MongoDB
        document = {
            "responseId": response.responseId,
            "submitter": response.submitter,
            "responses": response.responses,
            "submittedAt": datetime.now(UTC)
        }
        # Insert into MongoDB
        result = collection.insert_one(document)
        return {"message": "Response saved successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save response: {str(e)}")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
