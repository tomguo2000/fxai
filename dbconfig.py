import pymongo
from pymongo.errors import AutoReconnect
from config import CONFIG


def retry_if_auto_reconnect_error(exception):
    """Return True if we should retry (in this case when it's an AutoReconnect), False otherwise"""
    return isinstance(exception, AutoReconnect)

try:

    mongo = pymongo.MongoClient(CONFIG['dbserver'],connect=CONFIG['db_connect'])

    db = mongo['fuxi-service-ai']
    mongo.server_info()  #trigger exception if cannot connect to db

except:
    print("ERROR - Cannot connect to db")
    pass
