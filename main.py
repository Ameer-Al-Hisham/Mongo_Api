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
    data = collection1.find({},{"_id":0})
    for document in data:
      retdata.append(document)
      print(document)
    return jsonify(retdata)

@app.route("/findauser", methods=["GET"])
def findauser():
  uid = request.args.get("uid")
  data = collection1.find_one({"Uid": uid}, {"_id": 0})
  return jsonify(data)


@app.route("/usersignup",methods = ["POST"])
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


@app.route("/getalltask", methods=["GET"])
def getalltask():
  finlist = []
  data = collection2.find({"Status":"active"},{"_id":0,"Description":0})
  for doc in data:
    finlist.append(doc)
  return jsonify(finlist)
  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

