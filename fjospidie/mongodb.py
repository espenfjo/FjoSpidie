from pymongo import MongoClient
import gridfs
from Report import Transform


class MongoDB:
    def __init__(self, config):
        client = MongoClient(config.database_host)
        db = client.fjospidie
        self.collection = db.analysis
        self.fs = gridfs.GridFS(db)
        db.add_son_manipulator(Transform())

