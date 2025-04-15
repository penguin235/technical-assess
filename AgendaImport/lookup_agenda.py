from db_table import db_table
import pandas as pd
import argparse
import sys

def lookup(db_table, column, value):

    print("Retrieving all sessions and subsessions that match lookup parameters")

    # performing lookup 
    standard_return = sessions_table.select(['id', 'title', 'location', 'description', 'speaker', 'parent'], {column: value})
    print("Found the standard return value:", len(standard_return))
    for i in standard_return:
        print("ID:", i["id"], "Title:", i["title"])
    print()


    # check
    for i, v in enumerate(standard_return):
        if int(v["parent"]) < 0:
            # this is a session
            parent_key = v["id"]
            subsessions = sessions_table.select(['title', 'location', 'description', 'speaker'], {"parent": str(parent_key)})
            print("Adding a new subsessions:", subsessions)
            print()
            standard_return = standard_return[:i] + subsessions + standard_return[(i+1):]

    print("This is the final array: ", len(standard_return))

    """
    logic of function: 
    - go through all values of the table and get values that match the description (session or subsession regardless)
    - go through the return value, if something has parent of -1, that means that it is a session
        - check the table to see whether there are any subsession 
    """

def pretty_print(lookup_return):
    print("Pretty printing the lookup values")

if __name__ == "__main__":

    # parse command line arguments
    if len(sys.argv) < 3:
        print("Not enough arguments. Please try again with the following form: ")
        
    elif len(sys.argv) > 3:
        print("Too many arguments. Please try again with the following form: ")
        
    # check if legitmate column
    column = sys.argv[1]
    possible_columns = ["id", "date", "time_start", "time_end", "title", "location", "description", "speaker", "parent"]
    if column not in possible_columns:
        print("Please pick a valid column -can pick any of these: ")
    value = sys.argv[2]
    
    # creating schema for session table
    session_schema = {"ID": "integer PRIMARY KEY", "Date": "text", "Start_Time": "text", 
                      "End_Time": "text", "Session_Title": "text", "Location": "text",
                      "Description": "text", "Speakers": "text", "Parent": "text"}    

    # opening tables instance
    print("Opening table instance....")
    sessions_table = db_table("Sessions", session_schema)

    # Calling lookup according to user parameters
    print("Calling lookup on parameters")
    lookup(sessions_table, column, value)

    # select returns an array of values
    
    # testing subession



    
    