from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from models.student import Student, Address
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from bson import ObjectId  # Import ObjectId for converting string to ObjectId

from database import connect_to_mongo

router = APIRouter()

@router.post("/students", status_code=201)
async def create_student(student: Student):
    try:
        client = await connect_to_mongo()
        db = client["cosmo"]
        collection = db["students"]
        result = await collection.insert_one(student.dict())

        client.close()
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create student: {str(e)}")

@router.get("/students", response_model=List[Student])
async def list_students(country: Optional[str] = Query(None), age: Optional[int] = Query(None)):
    try:
        client = await connect_to_mongo()
        db = client["cosmo"]
        collection = db["students"]

        filter_params = {}
        if country:
            filter_params["address.country"] = country
        if age:
            filter_params["age"] = age

        students = await collection.find(filter_params).to_list(length=None)
        client.close()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list students: {str(e)}")

@router.get("/students/{id}", response_model=Student)
async def fetch_student(id: str = Path(..., description="The ID of the student")):
    try:
        client = await connect_to_mongo()
        db = client["cosmo"]
        collection = db["students"]

        object_id = ObjectId(id)
        student = await collection.find_one({"_id": object_id})
        client.close()

        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch student: {str(e)}")

@router.patch("/students/{id}", status_code=204)
async def update_student(student: Student, id: str = Path(..., description="The ID of the student")):
    try:
        client = await connect_to_mongo()
        db = client["cosmo"]
        collection = db["students"]

        object_id = ObjectId(id)
        await collection.update_one({"_id": object_id}, {"$set": student.dict(exclude_unset=True)})

        client.close()

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update student: {str(e)}")
    
@router.delete("/students/{id}")
async def delete_student(id: str = Path(..., description="The ID of the student")):
    try:
        client = await connect_to_mongo()
        db = client["cosmo"]
        collection = db["students"]
        object_id = ObjectId(id)
        result = await collection.delete_one({"_id": object_id})
        client.close()

        if result.deleted_count == 1:
            return {"message": "Student deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete student: {str(e)}")