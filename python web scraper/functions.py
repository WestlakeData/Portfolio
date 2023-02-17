import pandas as pd
import pyodbc
import requests
from sqlalchemy import create_engine, insert, select, Table, MetaData, and_
from bs4 import BeautifulSoup


def fetch_taxDistricts():
    engine = create_engine(
        'Connection String HERE'
    )
    connection = engine.connect()
    metadata = MetaData()




def fetchExistingRecords(yearString):
    engine = create_engine(
        'Connection String HERE'
    )
    connection = engine.connect()
    metadata = MetaData()
    uc = Table('Utah_County', metadata, autoload=True, autoload_with=engine)
    stmt = select([uc.columns.SerialNum]).where(and_(uc.columns.RecordYear == yearString, uc.columns.TMV == 0))
    results = connection.execute(stmt).fetchall()
    return results
    connection.close()


def clean_data(df, colname):
    df[colname] = (df[colname].str.replace('[\$,)]', '', regex=True)) \
        .str.replace('[(]', '-', regex=True)


def find_AllTables(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
    }
    try:
        # Get html from url
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            # Convert response object to soup object
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all tables in HTML
            tables = soup.find_all('table')
            return tables
        elif response.status_code == 500:
            print('Record no longer exists')
    except requests.exceptions.RequestException as e:
        # print URL with Errs
        raise SystemExit(f"{url}: is Not reachable \nErr: {e}")


def get_InfoTable(tablesData):
    # Read information table data to ls
    ls = pd.read_html(str(tablesData[2]))
    ls = [item[0] for item in ls]  # deconstruct list of lists
    sn = str([item[0] for item in ls])  # isolate SN data
    sn = sn[:-2]  # Remove last 2 characters from SN string
    sn = sn[-12:]  # Select last 12 characters from SN string
    acreage = str([item[4] for item in ls])  # isolate acreage data
    acreage = acreage[:-2]  # Remove last 2 characters from acreage string
    acreage = acreage[13:]  # Remove first 13 characters from acreage string
    return sn, acreage


def is_CY_updated(tablesData,CurrentYear):
    # Read Tax History data table
    ls = pd.read_html(str(tablesData[6]))
    # isolate Tax History years data
    year = [item[0] for item in ls]
    year = year[0]
    year = year[1]
    # isolate General Taxes data
    gt = [item[1] for item in ls]
    gt = gt[0]
    gt = float(str(gt[1]).replace('$', ''))
    if year == CurrentYear:
        if gt > 0:
            return True
        else:
            return False
    else:
        return False



# def get_ValueTable(tablesData):
#    # Read Value History data table
#    ls = pd.read_html(str(tablesData[5]))
#    # isolate valuation years data
#    year = [item[0] for item in ls]
#    year = year[0]
#    year = year[2:]


def Utah_Co_scraper(start, end):
    # Set headers to avoid 403 Forbidden Error
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
    }
    # Iterator Variable initiation
    c = 0
    no_page = 0
    step_count = start
    serial = start
    # Webpage url
    uc_website = 'https://www.utahcounty.gov/LandRecords/property.asp?av_serial='
    # Extract Record Data
    while serial <= end:
        try:
            url = uc_website + str(serial)
            # Get html from url
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                no_page = 0 # Reset no_page counter
                # Convert response object to soup object
                soup = BeautifulSoup(response.content, 'html.parser')
                # Find all tables in HTML
                tables = soup.find_all('table')

                sn, acreage = get_InfoTable(tables)

                # Read Value History data table
                ls = pd.read_html(str(tables[5]))
                # isolate valuation years data
                year = [item[0] for item in ls]
                year = year[0]
                year = year[2:]
                if len(year) > 0:
                    # isolate Commercial Real Estate Value data
                    ComREV = [item[1] for item in ls]
                    ComREV = ComREV[0]
                    ComREV = ComREV[2:]
                    # isolate Residential Real Estate Value data
                    ResREV = [item[2] for item in ls]
                    ResREV = ResREV[0]
                    ResREV = ResREV[2:]
                    # isolate Agricultural Real Estate Value data
                    AgREV = [item[3] for item in ls]
                    AgREV = AgREV[0]
                    AgREV = AgREV[2:]
                    # isolate Total Real Estate Value data
                    TotREV = [item[4] for item in ls]
                    TotREV = TotREV[0]
                    TotREV = TotREV[2:]
                    # isolate Commercial Improvements Value data
                    ComImp = [item[5] for item in ls]
                    ComImp = ComImp[0]
                    ComImp = ComImp[2:]
                    # isolate Residential Improvements Value data
                    ResImp = [item[6] for item in ls]
                    ResImp = ResImp[0]
                    ResImp = ResImp[2:]
                    # isolate Agricultural Improvements Value data
                    AgImp = [item[7] for item in ls]
                    AgImp = AgImp[0]
                    AgImp = AgImp[2:]
                    # isolate Total Improvements Value data
                    TotImp = [item[8] for item in ls]
                    TotImp = TotImp[0]
                    TotImp = TotImp[2:]
                    # isolate Greenbelt Land Value data
                    GB_Land = [item[9] for item in ls]
                    GB_Land = GB_Land[0]
                    GB_Land = GB_Land[2:]
                    # isolate Greenbelt Homesite Value data
                    GB_Home = [item[10] for item in ls]
                    GB_Home = GB_Home[0]
                    GB_Home = GB_Home[2:]
                    # isolate Greenbelt Total Value data
                    GB_Tot = [item[11] for item in ls]
                    GB_Tot = GB_Tot[0]
                    GB_Tot = GB_Tot[2:]
                    # isolate Total Market Value data
                    tmv = [item[12] for item in ls]
                    tmv = tmv[0]
                    tmv = tmv[2:]
                    # Create pandas DataFrame
                    value = {
                        'RecordYear': year, 'ComREV': ComREV, 'ResREV': ResREV, 'AgREV': AgREV, 'TotREV': TotREV,
                        'ComImprovement': ComImp, 'ResImprovement': ResImp, 'AgImprovement': AgImp,
                        'TotImprovement': TotImp,
                        'GB_Land': GB_Land, 'GB_Home': GB_Home, 'GB_Tot': GB_Tot, 'TMV': tmv
                    }
                    value = pd.DataFrame(value)

                    # Read Tax History data table
                    ls = pd.read_html(str(tables[6]))
                    # isolate Tax History years data
                    year = [item[0] for item in ls]
                    year = year[0]
                    year = year[1:]
                    # isolate General Taxes data
                    gt = [item[1] for item in ls]
                    gt = gt[0]
                    gt = gt[1:]
                    # isolate Adjustments data
                    adj = [item[2] for item in ls]
                    adj = adj[0]
                    adj = adj[1:]
                    # isolate Net Taxes data
                    net = [item[3] for item in ls]
                    net = net[0]
                    net = net[1:]
                    # isolate Fees data
                    fee = [item[4] for item in ls]
                    fee = fee[0]
                    fee = fee[1:]
                    # isolate Payments data
                    pay = [item[5] for item in ls]
                    pay = pay[0]
                    pay = pay[1:]
                    # isolate Tax Balance data
                    bal = [item[6] for item in ls]
                    bal = bal[0]
                    bal = bal[1:]
                    # isolate Balance Due data
                    due = [item[7] for item in ls]
                    due = due[0]
                    due = due[1:]

                    if any(due.str.contains('Click for Payoff')):
                        due = bal
                    # isolate Tax District data
                    dist = [item[8] for item in ls]
                    dist = dist[0]
                    dist = dist[1:]

                    # Create pandas DataFrame
                    taxHist = {
                        'RecordYear': year, 'GeneralTax': gt, 'Adjustment': adj, 'NetTax': net, 'Fee': fee,
                        'Payment': pay, 'TaxBalance': bal, 'BalanceDue': due, 'TaxDistrict': dist
                    }
                    taxHist = pd.DataFrame(taxHist)
                    # Join Tax History df and Valuation df
                    data = pd.merge(value, taxHist, how='right', on=['RecordYear'])

                    # Add SN data to df
                    data['SerialNum'] = sn
                    # Add acreage data to df
                    data['Acreage'] = acreage
                    # Add address data to df
                    # data['Address'] = address
                    # Correctly Format data
                    data['TaxDistrict'] = data['TaxDistrict'].str[:3]  # Select only numeric tax district

                    # data[['Street', 'City']] = data['Address'].str.split(' - ',
                    #                                                      expand=True)  # Separate Street and City in Address
                    # data = data.drop(columns='Address')  # Drop Address column

                    # List of columns to clean
                    clean_cols = [
                        'ComREV', 'ResREV', 'AgREV', 'TotREV',
                        'ComImprovement', 'ResImprovement', 'AgImprovement', 'TotImprovement',
                        'GB_Land', 'GB_Home', 'GB_Tot',
                        'TMV', 'GeneralTax', 'Adjustment',
                        'NetTax', 'Fee', 'Payment',
                        'TaxBalance', 'BalanceDue'
                    ]

                    for col in clean_cols:
                        clean_data(data, col)

                    # Dictionary of desired data types
                    col_dtype = {
                        'RecordYear': int, 'ComREV': int, 'ResREV': int, 'AgREV': int, 'TotREV': int,
                        'ComImprovement': int, 'ResImprovement': int, 'AgImprovement': int, 'TotImprovement': int,
                        'GB_Land': int, 'GB_Home': int, 'GB_Tot': int, 'TMV': int,
                        'GeneralTax': float, 'Adjustment': float, 'NetTax': float, 'Fee': float, 'Payment': float,
                        'TaxBalance': float, 'BalanceDue': float, 'Acreage': float
                    }
                    # Assign new datatypes
                    data = data.fillna(0).astype(col_dtype)

                    # Write to file
                    # data.to_csv('scraped_data_' + str(serial) + '.csv')
                    engine = create_engine(
                        'Connection String HERE'
                    )
                    connection = engine.connect()
                    # append the data from data to the "LandRecords" table via connection
                    data.to_sql(name='Utah_County', con=connection, if_exists='append', index=False)
                    connection.close()

                    # Iterate serial number
                    serial += 1
                    c += 1
                    print(str(c) + ' of ' + str(1+end - start) + ' Completed')

                else:
                    # Iterate serial number
                    serial += 1
                    c += 1
                    print(str(c) + ' of ' + str(1+end - start) + ' Completed')

            else:
                # After 5 500:Server Errors in a row, skip forward to next step
                if no_page >= 5:
                    step_count += 10000
                    serial = step_count
                    c = serial-start
                # Iterate counters by one
                else:
                    serial += 1
                    c += 1
                    no_page += 1
                print(str(c) + ' of ' + str(1+end - start) + ' Completed')

        except requests.exceptions.RequestException as e:
            # print URL with Errs
            raise SystemExit(f"{url}: is Not reachable \nErr: {e}")
