from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
  Base.metadata.create_all(engine)

  app.teardown_appcontext(close_db)
  # Now Flask will run close_db() together with its built-in teardown_appcontext() method. 
  # Note that we added app as a parameter of the init_db() function. We need to make sure that the variable gets passed in correctly.

def get_db():
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()
  return g.db

# The get_db() function now saves the current connection on the g object, if it's not already there.
# Then it returns the connection from the g object instead of creating a new Session instance each time.

# Whenever this function is called, it returns a new session-connection object. Other modules in the app can import Session directly from the db package,
# but using a function means that we can perform additional logic before creating the database connection.

# Note that the getenv() function is part of Python's built-in os module. But because we used a .env file to fake the environment variable, we need to first call load_dotenv() from the python-dotenv module. In production, DB_URL will be a proper environment variable.

# We also use several imported functions from sqlalchemy to create the following three important variables:

# The engine variable manages the overall connection to the database.

# The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.

# The Base class variable helps us map the models to real MySQL tables.

def close_db(e=None):
  db = g.pop('db', None)
  if db is not None:
    db.close()

# def init_db():
#   Base.metadata.create_all(engine)

# We're using the same Base.metadata.create_all() method from the seeds.py file, but we won't call it until after we've called init_db()