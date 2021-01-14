from flask_security import MongoEngineUserDatastore, Security

from data.MongoDB.db import db
from data.MongoDB_MongoEngine.models.roles import Role
from data.MongoDB_MongoEngine.models.users import User
from views import app

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)