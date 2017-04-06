import logging
import config
from pymongo import MongoClient
import time
import linecache
from multiprocessing import Process
'''
    logger is a wrapper around standard python logging that also sends log
    data to a mongoDB database when connection is available.
    If no connection is available, it issues a warning and caches the logs
    that have not been uploaded to upload later.
'''
class logger:

    def __init__(self):
        self.log = logging
        self.client = MongoClient ("mongodb://" + 
                                    config.mongo_user + ":" +
                                    config.mongo_pass + "@" +
                                    config.mongo_url)
        self.db = self.client.cuneyt_db
        self.log.basicConfig(filename = config.log_file, level = logging.DEBUG)
        self.connected = False
        self.backlog_index = 0
        self.backlog_process = Process(target = self.backlog)
            
    def cache(self, tp, data, t):
        with open(config.backlog_file, 'a') as backlog_file:
            backlog_file.write([tp, data, t])

    def insert(self, tp, data, t):
        succ = False
        try:
            if(self.db.log.insert_one ({"type" : tp,
                                        "time" : t,
                                        "data" : data})):
                self.connected = True
                return True
            else:
                self.connected = False
                #raise Exception("Not connected")
        except:
            cache(tp,data,t)
            return False
    
    def backlog(self):
        raise Exception("Not Yet Implemented")

    def debug(self, data):
        #succ = self.insert("debug", data, time.time())
        self.log.debug(data)

    def info(self, data):
        succ = self.insert("info", data, time.time())
        self.log.info(data)

    def warning(self, data):
        succ = self.insert("warning", data, time.time())
        self.log.warning(data)

    def error(self, data):
        succ = self.insert("error", data, time.time())
        self.log.error(data)

    def critical(self, data):
        succ = self.insert("critical", data, time.time())
        self.log.critical(data)
