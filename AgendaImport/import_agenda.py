from db_table import db_table
import pandas as pd
import argparse
import sys

"""
Inputs: excel file name
Ouputs: error if there is an issue, df if not issue
Function: opens excel file, puts excel information into a df, returns dataframe, closes excel file
"""

def create_df(ex_name):

    print("Opening excel file and creating data frame\n")
    print("Creating a data frame to make it easier to store into db...\n")
    df = pd.read_excel(ex_name, skiprows=14)
    print(df)
    return df

"""
Inputs: dataframe of an excel instance, db_instance
Ouputs: error if there is an issue
Function: puts df into a db

"""
def store_db(df, sessions_table):
    print("Storing df into a db instance...")

    prev_session = 0
    # TODO: add error handling for checking instances of tables and of df

    # value template
    value = {"ID": 0, 
            "date": "",
            "time_start": "",
            "time_end": "",
            "title": "", 
            "location": "",
            "description": "",
            "speaker": "",
            "parent": ""}
    
    for index, row in df.iterrows():

        temp_dict = row.to_dict()
        value["ID"] = index
        value["date"] = temp_dict['*Date']
        value["time_start"] = temp_dict['*Time Start']
        value["time_start"] = temp_dict['*Time End']
        value["title"] = temp_dict['*Session Title']
        value["location"] = temp_dict['Room/Location']
        value["description"] = temp_dict['Description']
        value["speaker"] = temp_dict['Speakers']
        
        if ((row['*Session or \nSub-session(Sub)']) == "Session"):
    
            value["parent"] = str(-1)
            sessions_table.insert(value)
            print("Succesfully added this -> session: ", value)
            print()
            prev_session = index

        if ((row['*Session or \nSub-session(Sub)']) == "Sub"):
            print("Entering sub function")

            value["parent"] = str(prev_session)
            sessions_table.insert(value)
            print("Succesfully added this -> subsession: ", value)
            print()
        
            

"""
Inputs: excel file (already opened), table 1, table 2
Ouputs: error if there is an issue
Function: calls other functions 

"""

def parse_store_excel(ex_name, sessions_table):


    print("Parsing excel file and storing into a data frame in parse_store_excel..\n")
    df = create_df(ex_name)

    # TODO: add error handling for invalid db
    
    print("Storing dataframe in db in parse_store_excel...\n")
    store_db(df, sessions_table)
    
########################################################

if __name__ == "__main__":

    # parse command line arguments
    print("Command line checks...")
    if len(sys.argv) < 2:
        print("Not enough arguments. Please try again with the following form: ")
        
    elif len(sys.argv) > 2:
        print("Too many arguments. Please try again with the following form: ")
        
    print("Entering main function...")
    excel_name = sys.argv[1]
    
    # creating schema for session
    session_schema = {"ID": "integer PRIMARY KEY", "date": "text", "time_start": "text", 
                      "time_end": "text", "title": "text", "location": "text",
                      "description": "text", "speaker": "text", "parent": "text"}    

    # creating tables instances
    print("Creating table instance....")
    sessions_table = db_table("Sessions", session_schema)
    
    # parsing and storing file in excel
    print("Calling parse_store_excel...")
    parse_store_excel(sessions_table)
    print("Parsing and storing completed")