from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security

from data.MongoDB_MongoEngine.models.roles import Role
from data.MongoDB_MongoEngine.models.users import User
from views import app

db = MongoEngine(app)

from data.MongoDB_MongoEngine.db import db

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)



