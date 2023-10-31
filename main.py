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

@app.route("/findauseremail", methods=["GET"])
def findauseremail():
  email = request.args.get("email")
  data = collection1.find_one({"Email": email}, {"_id": 0})
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


@app.route("/gettaskuid", methods=["GET"])
def gettaskuid():
  out = []
  uid = request.args.get("uid")
  data = collection1.find_one({"Uid": uid}, {"Availed_tasks": 1, "_id": 0})
  for i in data["Availed_tasks"]:
    if i["Status"] == "Success":
      out.append(i["Task_ID"])
  return jsonify(out)


@app.route("/getevaldetails", methods=["GET"])
def getevaldetails():
  taskid = request.args.get("taskid")
  uid = request.args.get("uid")
  out =[]
  print(taskid, uid)
  uidget = collection1.find_one({"Uid": uid}, {"_id": 0, "Availed_tasks": 1})
  for i in uidget["Availed_tasks"]:
    if i["Task_ID"] == taskid:
      out.append(i["Evaluation"])
  return jsonify(out[0])

@app.route("/gettaskdetails", methods=["GET"])
def gettaskdetails():
  task_id = request.args.get("taskid")
  data = collection2.find_one({"Tid": task_id}, {"_id": 0})
  if data != None:
    return jsonify(data)
  elif data == None:
    return jsonify("No task")


@app.route("/getprofilelink", methods=["GET"])
def getprofilelink():
  uid = request.args.get("uid")
  data = collection1.find_one({"Uid": uid}, {"_id": 0, "Profile_image": 1})
  return jsonify(data["Profile_image"])

@app.route("/getstatus", methods=["GET"])
def getstatus():
  uid = request.args.get('uid')
  tid = request.args.get('tid')
  data = collection1.find_one({"Uid": uid}, {"Availed_tasks": 1, "_id": 0})
  flag = 0
  for i in data["Availed_tasks"]:
    if i["Task_ID"] == tid and i["Status"] == "Success":
      flag = 1
      return jsonify('Success')
    elif i["Task_ID"] == tid and i["Status"] == "Failed":
      flag = 1
      return jsonify('Failed')
    elif i["Task_ID"] == tid and i["Status"] == "Ongoing":
      flag = 1
      return jsonify('Submit')
  if flag == 0:
    return jsonify("Register")


@app.route("/getUID", methods=["GET"])
def getUID():
  fuid = request.args.get('fuid')
  data = collection1.find_one({"Fireid": fuid}, {"Uid": 1, "_id": 0})
  return jsonify(data["Uid"])

@app.route("/registeratask", methods=["GET"])
def registeratask():
  uid = request.args.get('uid')
  tid = request.args.get('tid')
  data = {
    "Task_ID":tid,
    "Status" : "Ongoing"
  }
  collection1.update_one(
    {"Uid": uid},
    {"$push": {"Availed_tasks": data}}
)
  return jsonify("Success")


@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        data = request.get_json()
        user_email = data.get('email')
        updates = data.get('updates')  
        result = collection1.update_one({"Email": user_email}, {"$set": updates})

        if result.modified_count > 0:
            response = {"message": "User updated successfully"}
        else:
            response = {"message": "User not found or no updates were made"}

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/gettaskstatus", methods=["GET"])
def gettaskstatus():
  tid = request.args.get('tid')
  data = collection2.find_one({"Tid": tid}, {"_id": 0,"Status":1})
  if data != None:
    return jsonify(data["Status"])
  elif data == None:
    return jsonify("Not found")
  
@app.route("/addtask", methods=["POST"])
def addtask():
  try:
    data = request.get_json()
    collection2.insert_one(data)
    return jsonify("Success")
  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/updatetask', methods=['POST'])
def updatetask():
    try:
        data = request.get_json()
        tid = data.get('tid')
        updates = data.get('updates')  
        result = collection2.update_one({"Tid": tid}, {"$set": updates})

        if result.modified_count > 0:
            response = {"message": "User updated successfully"}
        else:
            response = {"message": "User not found or no updates were made"}

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/checkforeval', methods=['GET'])
def checkforeval():
  uid = request.args.get("uid")
  tid = request.args.get("tid")
  out = []
  data = collection1.find_one({"Uid":uid},{"_id":0,"Availed_tasks": 1})
  if data == None:
    return jsonify("User does not exsists")
  elif data != None:
    for i in data["Availed_tasks"]:
      if i["Task_ID"] == tid and i["Status"]  == "Success":
        out.append(i["Evaluation"])
      else:
        continue
    if len(out) == 0:
      return jsonify("Task unavailable or task status is not success")
    elif len(out)!=0:
      return jsonify(out[0])
    
@app.route('/updateeval', methods=['POST'])
def updateeval():
    try:
        data = request.get_json()
        uid = data.get('Uid')
        task_id = data.get('Task_ID')
        new_evaluation = data.get('New_Evaluation')

        result = collection1.update_one(
            {'Uid': uid, 'Availed_tasks.Task_ID': task_id},
            {'$set': {'Availed_tasks.$.Evaluation': new_evaluation}}
        )

        if result.modified_count > 0:
            return jsonify({'message': 'Evaluation updated successfully'}), 200
        else:
            return jsonify({'message': 'no updates were made'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


#Duplication may occur
@app.route('/update_user_self', methods=['POST'])
def update_user_self():
    try:
        data = request.get_json()
        user_uid = data.get('uid')
        updates = data.get('updates')
        experience = data.get('experience')
        respf = 0
        del data['experience']
        if experience != []:
          resp = collection1.update_one(
            {"Uid": user_uid},
            {"$push": {"Experience": experience}}
          )
          if resp.modified_count > 0:
            respf = 1
        result = collection1.update_one({"Uid": user_uid}, {"$set": updates})
        if result.modified_count > 0 or respf > 0:
            response = {"message": "User updated successfully"}
        else:
            response = {"message": "User not found or no updates were made"}

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
      
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=False)
