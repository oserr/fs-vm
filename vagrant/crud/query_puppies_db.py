from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from create_puppies_db import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

rows = session.query(Puppy).order_by(Puppy.name).all()
print('Puppies ordered by name')
print('(name)')
print('-----------------------')
for row in rows:
    print('({})'.format(row.name))
print()

six_months_ago = date.today() + relativedelta(months=-6)
rows = (session.query(Puppy)
        .filter(Puppy.dateOfBirth >= six_months_ago)
        .order_by(Puppy.dateOfBirth).all())
print('Puppies less than six months old')
print('(name, birthdate)')
print('--------------------------------')
for row in rows:
    print('({}, {})'.format(row.name, row.dateOfBirth))
print()

rows = session.query(Puppy).order_by(Puppy.weight).all()
print('Puppies ordered by ascending weight')
print('(name, weight)')
print('------------------------------------')
for row in rows:
    print('({}, {})'.format(row.name, row.weight))
print()

rows = (session.query(Puppy.shelter_id, func.count('*'))
         .group_by(Puppy.shelter_id).all())
print('Puppies grouped by shelter')
print('(shelter name, total puppies)')
print('------------------------')
for shelter_id, cnt in rows:
    shelter = session.query(Shelter).get(int(shelter_id))
    print('({}, {})'.format(shelter.name, cnt))
print()
