import pymongo
import certifi

con_str = "mongodb+srv://mia2380:FSDI1234@cluster0.wqcjjtt.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database('organikaBrenda')

me = {
    "first": "Brenda",
    "last": "Allemand",
    "age": 35,
    "hobbies": [],
    "address": {
        "street": "Evergreen",
        "number": 777,
        "city": "SoPi",
    }
}
