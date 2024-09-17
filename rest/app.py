from dataclasses import dataclass, field
from typing import Annotated, Optional, Union
from bson.objectid import ObjectId
from uuid import uuid4
from fastapi import Body, FastAPI
import pymongo

app = FastAPI(root_path="/api")
conn = pymongo.MongoClient("127.0.0.1", 27017)
db = conn["studentfdb"]


@dataclass()
class Student:
    name: str
    lastname: str
    phonenumber: str = ""
    score: float = 0
    grade: int = 0
    id_: Union[str, None] = field(default_factory=ObjectId)


class StudentUpdate(Student):
    phonenumber: Optional[str] = ""
    score: Optional[float] = None
    grade: Optional[int] = None


@app.get("/")
def sayHello():
    return dict(hello="world")


@app.get("/students")
def getStudents():
    students = list(db.student.find({}).limit(5))
    if not students:
        return {"students": []}
    for student in students:
        student["_id"] = str(student["_id"])
    return {"students": students}


@app.get("/students/{id_:str}")
def getStudent(id_: str):
    student = db.student.find_one({"_id": ObjectId(id_)})
    student["_id"] = str(student["_id"])
    return {"student": student}


@app.post("/students")
def createStudents(student:Annotated[StudentUpdate, Body(embed=True)]):
    print("Create:\t", student)
    new_student = {
        "name": student.name,
        "lastname": student.lastname,
        "phonenumber":student.phonenumber,
        "score": student.score,
        "grade": student.grade,
    }
    id_ = db.student.insert_one(new_student).inserted_id
    id_ = str(id_)
    return {"id": id_}


@app.put("/students/{id_:str}", response_model=None)
def updateStudents(id_: str, student: Annotated[StudentUpdate, Body(embed=True)]):
    de_student = getStudent(id_)["student"]
    new_student = {
        "name": student.name or de_student["name"],
        "lastname": student.lastname or de_student["lastname"],
        "phonenumber": student.phonenumber or de_student["phonenumber"],
        "score": student.score or de_student["score"],
        "grade": student.grade or de_student["grade"],
    }
    id_ = db.student.find_one_and_replace({"_id": ObjectId(id_)}, new_student)
    id_ = str(id_)
    return {"id": id_}


@app.delete("/students/{id_:str}")
def destroyStudents(id_: str):
    return db.student.delete_one({"_id": ObjectId(id_)}).acknowledged
