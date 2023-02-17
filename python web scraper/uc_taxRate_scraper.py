#Import
from functions import find_AllTables
from sqlalchemy import select, Table, create_engine, MetaData
import pandas as pd


# Year of tax rates to scrape as a String
year = '2021'
taxDistID= []
# Initialize connection and metadata
engine = create_engine(
        "CONNECTION STRING HERE"
        )
connection = engine.connect()
metadata = MetaData()
# Get taxDistrict table data
td = Table('taxDistrict', metadata, autoload=True, autoload_with=engine)
# Build select statement
stmt = select(td.columns.taxDistrictID)
# Get list of Tax Districts
taxDistricts = connection.execute(stmt).fetchall()
taxDistricts = [item[0].rstrip() for item in taxDistricts]
connection.close()

for taxDist in taxDistricts:
    url = 'https://www.utahcounty.gov/Dept/Treas/TaxRatesDistYrResults.asp?serialform-year=' + year + '&serialform-district=' + taxDist + '&yearform-submit=submit'
    tables = find_AllTables(url)
    
