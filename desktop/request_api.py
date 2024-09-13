import json
import requests

BASE_URL = "http://localhost:8008/api"


def listStudents():
    resp = requests.get(BASE_URL + "/students")
    students = resp.json()["students"]
    return students


def getStudent(id_):
    resp = requests.get(BASE_URL + "/students/" + str(id_))
    student = resp.json()["students"]
    return student


def createStudent(name, lastname, phnumber="", score=0, grade=0):
    student = {
        "name": name,
        "lastname": lastname,
        "phonenumber": phnumber,
        "score": score,
        "grade": grade,
    }
    data = json.dumps({"student": student})
    print(data)
    resp = requests.post(BASE_URL + "/students", data)
    print(resp.json())
    id_ = resp.json()["id"]
    return id_


def updateStudent(idx, name, lastname, phnumber="", score=None, grade=None):
    student = {
        "name": name,
        "lastname": lastname,
        "phonenumber": phnumber,
        "score": score,
        "grade": grade,
    }
    data = json.dumps({"student": student})
    print(data)
    resp = requests.put(BASE_URL + "/students/" + str(idx), data)
    print(resp.json())
    id_ = resp.json()["id"]
    return id_


def deleteStudent(id_):
    ok = requests.delete(BASE_URL + "/students/" + str(id_))
    return ok
