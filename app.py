from flask import Flask, jsonify, render_template, request
from utils import clean_dict_helper
import pymongo

app = Flask(__name__)
MONGO_URI = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
myclient = pymongo.MongoClient(MONGO_URI)
db = myclient["university"]


@app.route("/")
def index():
    return "Welcome to student management API!!"


@app.route("/get-students", methods=["GET"])
def get_students():
    students = list(db.student.find())
    if len(students) == 0:
        return jsonify({"success": False, "students": []}), 200
    return jsonify({"success": True, "students": clean_dict_helper(students)}), 200


@app.route("/get-student/<stud_id>", methods=["GET"])
def get_student(stud_id):
    # mongo_result = db.student.find_one({"id": stud_id})
    mongo_result = db.student.find_one({"_id": stud_id})

    print("DATA: ", mongo_result)
    # mongo_result = db.student.find_one({"id": 1})

    if mongo_result is None:
        return {
            "success": False,
            "message": "Student with ID: {} not found".format(stud_id),
            "data": mongo_result,
        }
    # return "YO"
    # return jsonify({"success": True, "message": clean_dict_helper(mongo_result)}), 200


@app.route("/add-student", methods=["POST"])
def add_student():
    student_schema = ["id", "name", "phone", "email", "subjects"]
    payload = request.json

    for required_key in student_schema:
        if required_key not in payload.keys():
            return jsonify({"message": "Missing {required_key} parameter"}), 400

    db.student.insert_one(payload)
    return jsonify({"success": True, "student": clean_dict_helper(payload)}), 201


@app.route("/update-student-name", methods=["POST"])
def update_user():
    payload = request.json
    stud_id = payload["student_id"]
    student_name = payload["student_name"]
    db.student.update_one({"id": stud_id}, {"$set": {"name": student_name}})
    return jsonify({"success": True, "message": clean_dict_helper(payload)})


@app.route("/update-student-email", methods=["POST"])
def update_email():
    payload = request.json
    stud_id = payload["student_id"]
    stud_email = payload["student_email"]
    db.student.update_one({"id": stud_id}, {"$set": {"email": stud_email}})
    return jsonify({"success": True, "message": clean_dict_helper(payload)})


@app.route("/GPA", methods=["POST"])
def GPA():
    payload = request.json
    gpa = payload["gpa"]
    return "your current GPA is  {}".format(gpa)


@app.route("/post_data", methods=["GET", "POST"])
def post_data():
    req_data = request.get_json()
    print(req_data)
    if "contact" not in req_data:
        return "contact is not givennnnn"
    if "firstname" not in req_data:
        return "First name is not here"
    if "lastname" not in req_data:
        return "LastName is not given"
    fname = req_data["firstname"]
    lname = req_data["lastname"]
    phone = req_data["contact"]
    return jsonify({"First Name": fname, "Last Name": lname, "Cell": phone})


if __name__ == "__main__":
    app.run()