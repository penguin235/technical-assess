from db_table import db_table
import pandas as pd

"""
Inputs: excel file name
Ouputs: error if there is an issue, df if not issue
Function: opens excel file, puts excel information into a df, returns dataframe, closes excel file
"""

def create_df(ex_name):

    print("Opening excel file and creating data frame\n")
    print("Creating a data frame to make it easier to store into db...\n")
    df = pd.read_excel(ex_name, skiprows=14)
    return df

"""
Inputs: dataframe of an excel instance, db_instance
Ouputs: error if there is an issue
Function: puts df into a db

"""
def store_db(df, sessions_table, sub_table):
    print("Storing df into a db instance...")

    # go through the rows of the dataframe
    
    # if something is of type session
        # insert into session table
        # update previous session trackers: prev_session = id
    # if something is of type subession
        # insert into subsession


"""
Inputs: excel file (already opened), table 1, table 2
Ouputs: error if there is an issue
Function: calls other functions 

"""

def parse_store_excel(ex_name, sessions_table, sub_table):


    print("Parsing excel file and storing into a data frame..\n")
    df = create_df(ex_name)
    if (not df):
        return "Error creating dataframe\n"
    
    print("Storing dataframe in db\n")
    store_db(df, sessions_table, sub_table)
    
########################################################

if __name__ == "__main__":
    print("Entering main function...")

    # creating schema for session
    session_schema = sub_schema = {"ID": int, "Date": "text", "Start_Time": "text",
                  "Session_Title": "text", "Location": "text",
                  "Description": "text", "Speakers": "text"}
    
    # creating a schema for subsessions
    sub_schema = {"ID": int, "Date": "text", "Start_Time": "text",
                  "Session_Title": "text", "Location": "text",
                  "Description": "text", "Speakers": "text", "Parent_ID": int}

    # creating tables instances
    #sessions_table = db_table("Session Table", session_schema)
    #sub_table = db_table("Subsession Table", sub_schema)

    # parsing and storing file in excel
    #parse_store_excel("agenda.xls", sessions_table, sub_table)