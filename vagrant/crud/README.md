# CRUD with python's sqlalchemy

* **C**reate
* **R**ead
* **U**pdate
* **D**elete

Scripts with examples to use python's *sqlalchemy* to create an [ORM][1] database.

## Prerequisites

* [python][2]
* python's [sqlalchemy][3]
* [sqlite][4]

## Example: dog shelters with puppies for adoption

### Defining the ORM entities and creating the DB

The `Shelter` entity.

```python
class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
```

The `Puppy` entity.

```python
class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Float)
```

To create the database, run `create_puppies_db.py`

```bash
python create_puppies_db.py
```

See `create_puppies_db.py` for more details with respect to what packages are
imported and to see how the tables are created in the last two lines of the script.

### Populating the DB with data

```bash
python puppypopulator.py
```

### Querying the DB

* Query all of the puppies and return the results in ascending alphabetical order
* Query all of the puppies that are less than 6 months old organized by the youngest
  first
* Query all puppies by ascending weight
* Query all puppies grouped by the shelter in which they are staying

```bash
python query_puppies_db.py
```

## Example: Simple restaurant names web page with BaseHTTPServer

### Defining the ORM entities and creating the DB

The `Restaurant` entity.

```python
class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
```

The `MenuItem` entity.

```python
class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
```

To create the database, run `database_setup.py`

```bash
python database_setup.py
```

### Populating the DB with data

```bash
python lotsofmenus.py
```

### Simple HTTP server with BaseHTTPServer

See `webserver.py` for all the details, but the gist is

* Define class that inherits from `BaseHTTPServer.BaseHTTPRequestHandler`.
* Define `do_GET(self)` to handle GET requests.
* Define `do_POST(self)` to handle POST requests.
* Create your HTTP server: `HTTPServer(('', port), YourHandler)`.
* Launch your server with `serve_forever()`.


[1]: https://en.wikipedia.org/wiki/Object-relational_mapping
[2]: https://www.python.org/downloads/
[3]: https://www.sqlalchemy.org/
[4]: https://www.sqlite.org/
