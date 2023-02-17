from sqlalchemy import (Table, Column, String, MetaData, create_engine, insert)
import csv

filepath = 'Path/To/File'

# Create connection string
engine = create_engine(
        'Connection String HERE'
    )
connection = engine.connect()
metadata = MetaData()
td = Table('taxDistrict', metadata, autoload = True, autoload_with = engine)
values_list = []
# Define taxDistrict table
# taxDistrict = Table('taxDistrict', metadata,
#                    Column('taxDistrictID', String(3)),
#                    Column('taxDistrictName', String(50)))
# Create table in database
# metadata.create_all(engine)

# Open data file
with open(filepath, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    row = next(reader)
    for row in reader:
        values_list.append(row)

stmt = insert(td)
result_proxy = connection.execute(stmt, values_list)
print(result_proxy.rowcount)

