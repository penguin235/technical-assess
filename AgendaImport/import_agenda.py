from db_table import db_table
from AgendaImport import agenda

"""
Inputs: name of an excel file
Ouputs: bool if file opened or not (True = opened, False = not opened)
Function: checks to see if excel file can be openend
"""

def open_excel(ex_name):
    print("Opening excel file...")

"""
Inputs: excel file (already opened), db_instance
Ouputs: error if there is an issue
Function: puts excel information into a df 

"""

def create_df(ex_name):
    print("Creating a data frame to make it easier to store into db...")

"""
Inputs: dataframe of an excel instance, db_instance
Ouputs: error if there is an issue
Function: puts df into a db

"""
def store_db(df, db_instance):
    print("Storing df into a db instance...")


"""
Inputs: excel file (already opened), db_instance
Ouputs: error if there is an issue
Function: calls other functions 

"""

def parse_store_excel(ex_name, db_instance):

    print("Opening excel file...")
    if ( not open_excel(ex_name)):
        return "Error opening excel file..."
    
    print("Parsing excel file and storing into a data frame..")
    df = create_df(ex_name)
    if (not df):
        return "Error create dataframe"
    
    print("Storing dataframe in db")
    store_db(df, db_instance)
    
########################################################
"""
Inputs: 
Outputs:
Function: 
"""
def create_schema():

    print("Creating a table schema...")



if __init__ == "main":
    print("Entering main function...")

    # creating schema
    schema = create_schema()
    
    # creating a db instance
    db_instance = db_table("Agenda Tables", schema)

    # storing excel db file into db
    parse_store_excel("agenda.xls", db_instance)