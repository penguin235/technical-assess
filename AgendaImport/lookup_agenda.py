from types import NoneType
from db_table import db_table
import pandas as pd
import argparse
import sys
import tabulate

def lookup(sessions_table, column, value):

    print("Retrieving all sessions and subsessions that match lookup parameters...")

    # performing lookup on all sessions and subsession
    standard_return = sessions_table.select(['id', 'title', 'location', 'description', 'speaker', 'parent', 'parent_title'], {column: value})
    print("Extracted", len(standard_return), " sessions and subsessions that match this parameter")
    for i in standard_return:
        print("ID:", i["id"], " | Title:", i["title"], " | Parent:", i["parent"])
    print()

    print("Retrieving subsessions of selected sessions...")
    # check for subsections within the standard array

    # somethings going wrong here
    for i, v in enumerate(standard_return):
        if int(v["parent"]) < 0:
            # this is a session
            parent_key = v["id"]
            parent_title = v["title"]
            subsessions = sessions_table.select(['id', 'title', 'location', 'description', 'speaker', 'parent', 'parent_title'], {"parent": str(parent_key)})
            # print("Adding a collection of subsessions:", subsessions)
            standard_return += subsessions

    print("This is the final collection of sessions and subsessions that match " \
          "parameters along with subsessions that are affiliated with selected sessions: ",
        len(standard_return))
    for i in standard_return:
        print("ID:", i["id"], "| Title:", i["title"], " | Parent_Title:", i["parent_title"])
    print()

    return standard_return
 

def pretty_print(lookup_return):
    print("Pretty printing the lookup values...")
    print("Creating chart/table...")

    # what to print: Title, Location, Description, Session/Subsession of What
    tabulate_table = []
    for i in lookup_return:
        # print("processing this item right now: ", i)
        entry = []

        # building output string
        # output_string = i["title"] + "      " 
        if isinstance(i["title"], str) and len(i["title"]) < 60:
            # output_string += (i["description"]) + "      "
            entry.append(i["title"])
        elif isinstance(i["title"], str) and len(i["title"]) > 60:
            # output_string += (i["description"])[:30] + "..." + "      "
            entry.append((i["title"])[:60])
        elif isinstance(i["title"], NoneType):
            # output_string += "      "
            entry.append("")
        
        
        # type checking for location
        if isinstance(i["location"], NoneType):
            # output_string += "      "
            entry.append("")
        else:
            # output_string += i["location"] + "      "
            entry.append(i["location"])

        
        # type and size checking for description
        if isinstance(i["description"], str) and len(i["description"]) < 40:
            # output_string += (i["description"]) + "      "
            entry.append(i["description"])
        elif isinstance(i["description"], str) and len(i["description"]) > 40:
            # output_string += (i["description"])[:30] + "..." + "      "
            entry.append((i["description"])[:40])
        elif isinstance(i["description"], NoneType):
            # output_string += "" + "      "
            entry.append("")

        # printing if session or subsession
        if(int(i["parent"]) < 0):
            # output_string += "Session"
            entry.append("Session")
        else:
            # output_string += "Session of " + i["parent_title"]
            entry.append("Session of " + i["parent_title"])
        
        #print(output_string)
        tabulate_table.append(entry)
    
    table = tabulate.tabulate(
        tabulate_table,
        headers = ["Session Title", "Location", "Abrreviated Description", "Session or Subsession"],
        tablefmt="grid"
    )
    
    print(table)


if __name__ == "__main__":

    # parse command line arguments
    if len(sys.argv) < 3:
        print("Not enough arguments. Please try again with the following form: ")
        
    elif len(sys.argv) > 3:
        print("Too many arguments. Please try again with the following form: ")
        
    # check if legitmate column
    column = sys.argv[1]
    # TODO: remove id and parent from user-facing options
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
    print("Calling lookup on parameters...")
    sessions = lookup(sessions_table, column, value)

    # Taking all the valid sessions and printing them in a table format
    pretty_print(sessions)



    
    