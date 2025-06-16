from peewee import *
from flask_login import UserMixin
import os

# ✅ Connect to SQLite database
db = SqliteDatabase('database.db')


# ✅ Base model to bind all tables to the same DB
class BaseModel(Model):
    class Meta:
        database = db


# ✅ User model for authentication & profile
class User(BaseModel, UserMixin):
    name = CharField()
    email = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()
    dob = CharField(null=True)              # Date of Birth
    program = CharField()                   # Diploma / Degree
    course = CharField()                    # Course name
    avatar_url = CharField()                # DiceBear avatar URL


# ✅ Project model for user projects
class Project(BaseModel):
    title = CharField()
    description = TextField()
    github_url = CharField(null=True)
    tech_stack = CharField(null=True)
    team_members = CharField(null=True, default="")  # Comma-separated
    is_favorite = BooleanField(default=False)
    user = ForeignKeyField(User, backref='projects')


# ✅ DB initialization helper
def initialize_db():
    """Call once to create the DB and tables if they don't exist."""
    if not os.path.exists("database.db"):
        db.connect()
        db.create_tables([User, Project])
        db.close()
