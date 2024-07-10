from sqlalchemy.ext.automap import automap_base
from repository.engine import engine

Base = automap_base() # Create a base class for the automap schema


Base.prepare(autoload_with=engine) # Reflect the tables in the database

# For each class in Base.classes, create a class in the data_model.model module
for class_ in Base.classes:
    globals()[class_.__name__.capitalize()] = class_

print(globals())






    


