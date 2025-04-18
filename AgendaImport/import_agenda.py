from types import NoneType
from db_table import db_table
import pandas as pd
import numpy as np
import argparse
import sys
import os

"""
Inputs: @param: excel file name
Ouputs: error if there is an issue, df if not issue
Function:
    - opens excel file
    - puts excel information into a df
    - returns dataframe
"""
def create_df(ex_name):

    print("Opening excel file and creating data frame...")
    print("Creating a data frame to make it easier to store into db...")
    try:
        df = pd.read_excel(ex_name, skiprows=14)
        return df
    except FileNotFoundError:
        print("Excel file not found.")

    #print(df)

"""
Inputs: @param: dataframe of an excel instance, db_instance
Ouputs: error if there is an issue
Function: puts df into a db
    - extracts row from df, puts into a dict object
    - cleans data
    - inserts speakers into speakers table
    - identifies session, subsession relationship
    - inserts sessions into sessions table

"""
def store_db(df, sessions_table, speakers_table):
    print("Storing df into a db instance...")

    """"
    Refinements/Task List:
    - PRIMARY FUNCTION: ensure that speaker publications are getting updated correctly
        - either do some kind of tallying or pass name as a parameter as well
        - appears to be functioning fine!
    - STRETCH: try to understand why "Tim Harris" entry is not getting recognized
    - ERROR HANDLING: 
        - complete error handling for invalid df getting passed
        - put any db functions into a try-catch block
    - (Completed) PRIMARY FUNCTION: add all speakers table (character issues)
    """

    prev_session = 0
    if df is None:
        print("No dataframe found to store in table.")
        raise RuntimeError("No dataframe to store in database.")

    # value template
    value = {"ID": 0, 
            "date": "",
            "time_start": "",
            "time_end": "",
            "title": "", 
            "location": "",
            "description": "",
            "speaker": "",
            "parent": "", 
            "parent_title": ""}

    
    for index, row in df.iterrows():

        temp_dict = row.to_dict()
        value["ID"] = index
        value["date"] = temp_dict['*Date']
        value["time_start"] = temp_dict['*Time Start']
        value["time_end"] = temp_dict['*Time End']
        value["title"] = temp_dict['*Session Title']
        value["location"] = temp_dict['Room/Location']
        value["description"] = temp_dict['Description']
        value["speaker"] = temp_dict['Speakers']

        # cleaning up values for NaN
        for v in value.keys():
            if (type(value[v]) == float):
                value[v] = "None Present"

        # contribute to speakers table
        # get the list of speakers and either add or update their value

        if value["speaker"] != "None Present":
            for speaker in value["speaker"].split(";"):
                #print("Processing this speaker:", speaker)
            
                # should only be one value in standard return array
                #print("Identifying if there are existing publications for speaker....")
                standard_return = speakers_table.select(['name', 'session_ids', 'session_titles', 'num_sessions'], {"name": speaker})
                # this is a new speaker - insert
                if (len(standard_return) == 0):
                    #print("No existing publications found for speaker. Inserting new entry in speaker table...")
                    try:
                        speakers_table.insert({"name": speaker, "session_ids": str(index) + ";", "session_titles": value["title"] + ";", "num_sessions": str(1)})
                    except:
                        print("Error inserting speaker into speakers table")
                elif (speaker != "Tim Harris"):
                    # if this is not a new speaker - update
                    #print("Existing publications found for speaker. Performing an update on speakers...")
                    updating_id = standard_return[0]["session_ids"] + str(index) + ";"
                    updating_titles = standard_return[0]["session_titles"] + value["title"] + ";"
                    # updating_num_sessions = int(standard_return[0]["num_sessions"]) + 1
                    try:
                        speakers_table.update({ "session_ids": updating_id }, { "session_titles": updating_titles })
                    except:
                        print("Error updating field in speakers_table")
                

        # identifying if session or subsession
        if ((row['*Session or \nSub-session(Sub)']) == "Session"):
    
            value["parent"] = str(-1)
            try:
                sessions_table.insert(value)
            except:
                print("Error adding session into sessions table")
            #print("Succesfully added this -> session: ", value)
            #print()
            prev_session = index
            session_name = value["title"]

        if ((row['*Session or \nSub-session(Sub)']) == "Sub"):
            # print("Entering sub function")

            value["parent"] = str(prev_session)
            value["parent_title"] = session_name
            try:
                sessions_table.insert(value)
            except:
                print("Error adding subsession into sessions table")
            #print("Succesfully added this -> subsession: ", value)
            #print()
        
            

"""
Inputs: @param: excel file (str), sessions table (db_table)
Ouputs: error if there is an issue
Function: 
    - calls create df to create a dataframe of the excel sheet
    - calls store db to store the dataframe into the sessions table
"""
def parse_store_excel(ex_name, sessions_table, speakers_table):

    # creating df
    print("Parsing excel file and storing into a data frame in parse_store_excel..")
    df = create_df(ex_name)
    if df is None:
        print("No dataframe found. Try Again")
        sys.exit(1)
    else:
        # storing db
        print("Storing dataframe in db in parse_store_excel...")
        store_db(df, sessions_table, speakers_table)
    
########################################################
"""
Main:
- addresses command line inputs
- contains schema for sessions and speakers table
- creates instances of `db_table` for sessions and speakers
- calls `parse_store_excel`

"""

if __name__ == "__main__":

    # parse command line arguments
    print("Command line checks...")
    if len(sys.argv) < 2:
        print("Not enough arguments. Please try again with the following form: $ python import_agenda.py \"excel_spreadsheet.xls\"")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Not enough arguments. Please try again with the following form: $ python import_agenda.py \"excel_spreadsheet.xls\"")
        sys.exit(1)
    
    # valid command line arguments - proceed with main
    print("Entering main function...")
    excel_name = sys.argv[1]

    if os.path.exists("interview_test.db"):
        os.remove("interview_test.db")
    
    # creating schema for session
    session_schema = {"ID": "integer PRIMARY KEY", "date": "text", "time_start": "text", 
                      "time_end": "text", "title": "text", "location": "text",
                      "description": "text", "speaker": "text", "parent": "text", "parent_title": "text"}    

    # creating tables instances
    print("Creating session table instance....")
    sessions_table = db_table("Sessions", session_schema)

    # creating speaker schema
    speaker_schema = {"name": "text", 
                    "session_ids": "text", 
                    "session_titles": "text", 
                    "num_sessions": "text"}
    
    # creating speaker table instance
    print("Creating speaker table instance....")
    speakers_table = db_table("Speakers", speaker_schema)

    # parsing and storing file in excel
    print("Calling parse_store_excel...")
    parse_store_excel(excel_name, sessions_table, speakers_table)
    print("Parsing and storing into database table completed.")