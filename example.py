'''

  flask-ponywhoosh example
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Perform full-text searches over your database with Pony ORM and PonyWhoosh,
  for flask applications.

  :copyright: (c) 2015-2018 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

import os
import json

from datetime               import datetime, timedelta, date
from flask                  import Flask, jsonify, render_template
from flask_bootstrap        import Bootstrap
from flask_ponywhoosh       import PonyWhoosh
from flask_script           import Manager, Shell
from pony.orm               import *
from pony.orm.serialization import to_json


app         = Flask(__name__)
app.debug   = True

manager = Manager(app)
manager.add_command("shell", Shell(use_bpython=True))

# -----------------------------------------------------------------------------
#
# Options for PonyWhoosh package
#
# -----------------------------------------------------------------------------

app.config['PONYWHOOSH_DEBUG']              = True
app.config['PONYWHOOSH_DIR']                = 'whooshes'
app.config['PONYWHOOSH_MIN_STRING_LEN']     = 1
app.config['PONYWHOOSH_URL_ROUTE']          = '/'
app.config['PONYWHOOSH_WRITER_TIMEOUT']     = 3
app.config['SECRET_KEY']                    = 'hard to guess string'

# -----------------------------------------------------------------------------

bootstrap   = Bootstrap(app)
db          = Database()
pw          = PonyWhoosh(app)

@pw.register_model('business_name','tags','location','category')
class Business(db.Entity):
  number  = PrimaryKey(int, auto=True)
  business_name = Required(str, unique=True)
  address  = Optional(str)
  phone = Optional(str)
  email = Optional(str)
  website = Optional(str)
  category = Optional(str)
  location = Optional(str)
  tags = Optional(str)
  description = Optional(str)
  # picture   = Optional(buffer, lazy=True)

db.bind('sqlite', 'example.sqlite', create_db=True)
#db.bind('mysql', host="localhost", user="pony", passwd="pony", db="university1")
#db.bind('postgres', user='pony', password='pony', host='localhost'
#  , database='university1')
#db.bind('oracle', 'university1/pony@localhost')


db.generate_mapping(create_tables=True)


@db_session
def populate_database():
  if select(s for s in Business).count() > 0: return
  # b1 = Business(
  #   business_name="JELANI BEAUTY SUPPLY STORE", 
  #   address="4425 SKIDAWAY ROAD, SAVANNAH, GEORGIA 31405",
  #   phone="912-777-4978", 
  #   email="JELANIBEAUTYSUPPLY@GMAIL.COM",
  #   website="WWW.JELANIBEAUTYSUPPLY.COM",
  #   category="Baby Essentials, Beauty, Beauty Supply Store, Cosmetics, Footwear, Grooming Products, Hair Care Products, Jewelry & Accessories, Personal Care, Skin Care Products",
  #   location="Georgia, Savannah",
  #   tags="Beauty Supply Store, BLACKOWNEDBEAUTYSUPPLY, cosmetics, georgia, HAIR STORE, MINORITYOWNED, savannah, SAVANNAH STATE, WOMENOWNED"
  # )
  data = json.load(open('data.json', 'r'))
  for obj in data:
    flag = True
    for k,v in obj.items():
      if v == None:
        flag = False
        break
    if flag:
      print(obj['business_name'])
      b = Business(
        business_name=obj['business_name'], 
        address=obj['Address'],
        phone=obj['Phone'], 
        email=obj['Email_ID'],
        website=obj['Website'],
        category=obj['Category'],
        location=obj['Location'],
        tags=obj['Tags']
      )
  commit()

@app.route("/database")
@db_session
def index():
  return to_json(Business.select())

if __name__ == "__main__":
  populate_database()
  manager.run()
