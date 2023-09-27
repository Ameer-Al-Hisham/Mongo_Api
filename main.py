from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo

# Replace with your own MongoDB Atlas connection string
connection_string = "mongodb+srv://enragedgamer007:4YVkFDprOAHtGOI9@cluster0.mwtqfms.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient instance
client = pymongo.MongoClient(connection_string)

db1 = client["database1"]
collection1 = db1["collection1"]
collection2 = db1["collection2"]

# Flask
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
  return "Hello world"


@app.route("/viewusers", methods=["GET"])
def viewusers():
  retdata = []
  data = collection1.find({}, {"_id": 0})
  for document in data:
    retdata.append(document)
    print(document)
  return jsonify(retdata)


@app.route("/findauser", methods=["GET"])
def findauser():
  uid = request.args.get("uid")
  data = collection1.find_one({"Uid": uid}, {"_id": 0})
  return jsonify(data)


@app.route("/usersignup", methods=["POST"])
def usersignup():
  try:
    data = request.get_json()
    collection1.insert_one(data)
    return "Success"
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route("/getregcount", methods=["GET"])
def getregcount():
  data = collection1.count_documents({})
  return jsonify(data)


@app.route("/getallactive", methods=["GET"])
def getallactive():
  finlist = []
  data = collection2.find({"Status": "active"}, {"_id": 0, "Tid": 1})
  for doc in data:
    finlist.append(doc["Tid"])
  return jsonify(finlist)


@app.route("/getoneongoing", methods=["GET"])
def getoneongoing():
  uid = request.args.get('uid')
  finlist = []
  data = collection1.find_one({"Uid": uid}, {"Availed_tasks": 1, "_id": 0})
  for i in data["Availed_tasks"]:
    if i["Status"] == "Ongoing":
      finlist.append(i["Task_ID"])
  return jsonify(finlist)


@app.route("/getoneavailed", methods=["GET"])
def getoneavailed():
  out = []
  uid = request.args.get('uid')
  data = collection1.find_one({"Uid": uid}, {"Availed_tasks": 1, "_id": 0})
  for i in data["Availed_tasks"]:
    out.append(i["Task_ID"])
  return jsonify(out)

@app.route("/getstatus", methods=["GET"])
def getstatus():
  uid = request.args.get('uid')
  tid = request.args.get('tid')
  data = collection1.find_one({"Uid": uid}, {"Availed_tasks": 1, "_id": 0})
  for i in data["Availed_tasks"]:
    if i["Task_ID"] == tid and i["Status"] == "Success":
      return jsonify('Success')
    elif i["Task_ID"] == tid and i["Status"] == "Failed":
      return jsonify('Failed')
    elif i["Task_ID"] == tid and i["Status"] == "Ongoing":
      return jsonify('Ongoing')

@app.route("/gettaskuid", methods=["GET"])
def gettaskuid():
  out = []
  uid = request.args.get("uid")
  data = collection1.find_one({"Uid": uid}, {"Availed_tasks": 1, "_id": 0})
  for i in data["Availed_tasks"]:
    if i["Status"] == "Success":
      out.append(i)
  return jsonify(out)


@app.route("/getevaldetails", methods=["GET"])
def getevaldetails():
  taskid = request.args.get("taskid")
  uid = request.args.get("uid")
  print(taskid, uid)
  # Define the filter criteria
  filter_criteria = {
    "Uid": uid,
    "availed_tasks": {
      "$elemMatch": {
        "task_id": taskid
      }
    }
  }
  projection = {"_id": 0, "availed_tasks.$": 1}
  data = []
  cursor = collection1.find(filter_criteria, projection)
  for doc in cursor:
    availed_tasks = doc.get("availed_tasks", [])
    for task in availed_tasks:
      if task.get("task_id") == taskid:
        data.append(task["evaluation"])
  if len(data) == 1:
    return jsonify(data[0])
  else:
    return "internal error"


@app.route("/gettaskdetails", methods=["GET"])
def gettaskdetails():
  task_id = request.args.get("taskid")
  data = collection2.find_one({"Tid": task_id}, {"_id": 0})
  return jsonify(data)


@app.route("/getprofilelink", methods=["GET"])
def getprofilelink():
  uid = request.args.get("uid")
  data = collection1.find_one({"Uid": uid}, {"_id": 0, "Profile_image": 1})
  return jsonify(data["Profile_image"])

  collection1.insert_one(data)
  return "Success"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=False)