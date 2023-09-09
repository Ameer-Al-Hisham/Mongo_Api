from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo


# Replace with your own MongoDB Atlas connection string
connection_string = "mongodb+srv://enragedgamer007:4YVkFDprOAHtGOI9@cluster0.mwtqfms.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient instance
client = pymongo.MongoClient(connection_string)

db1 = client["database1"]
collection1 = db1["collection1"]


# Flask
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Hello world"


@app.route("/viewall", methods=["GET"])
def viewall():
    retdata = []
    data = collection1.find({},{"_id":0})
    for document in data:
      retdata.append(document)
      print(document)
    return jsonify(retdata)

@app.route("/viewone", methods=["GET"])
def viewone():
  uid = request.args.get("uid")
  data = collection1.find_one({"Uid": uid}, {"_id": 0})
  return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


