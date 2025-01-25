from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()
client = MongoClient('your_mongodb_uri')  # Replace with your MongoDB URI
db = client['log_database']

@app.get("/logs")
def get_logs(log_level: str = None, start_time: str = None, end_time: str = None):
    query = {}
    
    if log_level:
        query['log_level'] = log_level
    
    if start_time and end_time:
        query['timestamp'] = {'$gte': start_time, '$lte': end_time}

    logs = list(db.logs.find(query))
    
    return {"logs": logs}
