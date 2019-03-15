# We use sqlite to testing in this POC , you can choose other database for
# final results.

# CAUTION !!! This script delete SQLite database file
# and create new one if database exists

import os
import sys
import DatabaseModels
import Constants


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

def createDatabase():
  try:
    # delete sqlite file if exists. Remove if you use other database
    if os.path.exists(Constants.SQLLite_file):
      print("The file knows_unknows.db  exist, do nothing")
      # os.remove(Constants.SQLLite_file)
    else:
      print("The file knows_unknows.db does not exist, creating in " + Constants.SQLLite_Base_URL)
      # Create an engine that stores data in the local directory's
      # knows_unknows.db file.
      engine = create_engine(Constants.SQLLite_Base_URL)

      # Create all tables in the engine. This is equivalent to "Create Table"
      # statements in raw SQL.
      DatabaseModels.Base.metadata.create_all(engine)
  except:
    print("Something went wrong. This must be usual in starting process if "
          "other threat create the database")


