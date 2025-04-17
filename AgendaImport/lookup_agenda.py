from types import NoneType
from db_table import db_table
import pandas as pd
import argparse
import sys
import tabulate


"""
Input: @param: sessions_table, column, value
Output: array of all sessions and subsessions that match the query value
Function:
    - Extracts sessions and subsessions that directly match the parameter
    - Goes through the sessions and extracts associated subsessions
"""
def lookup(sessions_table, column, value):

   
    print("Retrieving all sessions and subsessions that match lookup parameters...")

    # performing lookup on all sessions and subsession
    # retrieving all values instead of just a select few

    standard_return = sessions_table.select(['id', 'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker', 'parent', 'parent_title'], {column: value})
    print("Extracted", len(standard_return), "sessions and subsessions that match this parameter.")

    """
    # parse through for speakers, etc. just to make sure information is accurate
    for i in standard_return:
        print("ID:", i["id"], " | Title:", i["title"], " | Parent:", i["parent"])
    print()
    """
    
    print("Retrieving subsessions of selected sessions...")
    # check for subsections within the standard array

    # earlier statment saying something was going wrong here - confirm proper function
    for i, v in enumerate(standard_return):
        if int(v["parent"]) < 0:
            # this is a session
            parent_key = v["id"]
            subsessions = sessions_table.select(['id', 'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker', 'parent', 'parent_title'], {"parent": str(parent_key)})
            # print("Adding a collection of subsessions:", subsessions)
            standard_return += subsessions
    
    """
    print("This is the final collection of sessions and subsessions that match " \
          "parameters along with subsessions that are affiliated with selected sessions: ",
        len(standard_return))
    for i in standard_return:
        print("ID:", i["id"], "| Title:", i["title"], " | Parent_Title:", i["parent_title"])
    print()
    """
    return standard_return


"""
Input: @param: speaker
Output: Error if it is a certain speaker
Function:
    - does a query on the speakers table to identify what sessions the speaker is associated
    - calls lookup on all the sessions the speaker is associcated with
"""
def speaker_query(speaker):

    # error handling
    if (speaker =="Tim Harris"):
        print("Unable to process request, please try with another speaker.")
        sys.exit(1)
    
    standard_return = speakers_table.select(['name', 'session_ids', 'session_titles', 'num_sessions'], {"name": speaker})
    # getting all the sessions that this speaker is in
    if (len(standard_return) == 0):
        print("No sessions found for this speaker.")
        return []
    speaker_sessions = standard_return[0]["session_titles"].split(";")
    # prepping the array that will get returned
    return_array = []
    for s in speaker_sessions:
        print("Calling internal lookup on this session the speaker is involved in:", s)
        return_array += lookup(sessions_table, "title", s)

    return return_array

"""
Input: @params: lookup_return array
Output: pretty printed output of query
Function:
    - only prints out spreadsheet information. nothing about the id of session
    - uses spacing and indenting for a cleaner output
"""
def pretty_print(lookup_return):

    print("Pretty printing the lookup values...")
    if (len(lookup_return) == 0):
        print()
        print("No results found for query. If this is unexpected behavior, please refer to \"User_Guide_and_Documentation.md\" for proper input formatting.")

    # returned values: 'id', 'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker', 'parent', 'parent_title']
    # printed values:  'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker'

    count = 1 
    for i in lookup_return:
        # print("processing this item right now: ", i)
        counting = str(count) + ")"
        print(counting)
        print("---->", i["title"] )
        print("--------> Date: ", i["date"])
        print("--------> Start Time: ", i["time_start"])
        print("--------> End Time", i["time_end"])
        print("--------> Location: ", i["location"])
        print("--------> Speakers:", i["speaker"])

        if(int(i["parent"]) < 0):
            # output_string += "Session"
            #entry.append("Session")
            print("--------> Session or Subsession: Session")
        else:
            # output_string += "Session of " + i["parent_title"]
            print("--------> Session or Subsession: Subsession of",  i["parent_title"])
        
        print("--------> Description:", i["description"])
        print()
        print("=====================================================================")
        count += 1
"""
Main:
- addresses command line inputs
- contains schema for sessions and speakers table
- creates instances of `db_table` for sessions and speakers
- calls either speaker_query or lookup depending on command line input
"""


if __name__ == "__main__":

    """
    Refinements/Tasks
    - PRIMARY FUNCTION: raise error instead of doing sys.exit()
    """

    # parse command line arguments
    if len(sys.argv) < 3:
        print("Not enough arguments. Please try again with the following form: $ python lookup_agenda.py \"column\" \"value\"")
        sys.exit()
    elif len(sys.argv) > 3:
        print("Too many arguments. Please try again with the following form: $ python lookup_agenda.py \"column\" \"value\" ")
        print("If your column or value argument is more than one word, please use the following format: $ python lookup_agenda.py \"column\" \"value\"")
        sys.exit()
        
    # check if legitmate column
    column = sys.argv[1]
    possible_columns = ["date", "time_start", "time_end", "title", "location", "description", "speaker"]
    if column not in possible_columns:
        print("Please pick a valid column out of the following selection: date, time_start, time_end, title, location, description, speaker")
        sys.exit()
    
    value = sys.argv[2]
    
    # cleaning up values for NaN, presence of apostrophe
       
    if (type(value) == str) and ("\'" in value):
        (value).replace('\'', '\"')
        #print("Changed!", value)
    
    # set value parameter
    
    # creating schema for session table
    session_schema = {"ID": "integer PRIMARY KEY", "date": "text", "time_start": "text", 
                      "time_end": "text", "title": "text", "location": "text",
                      "description": "text", "speaker": "text", "parent": "text", "parent_title": "text"} 

    # opening tables instance
    print("Opening sessions table instance....")
    sessions_table = db_table("Sessions", session_schema)

    speaker_schema = {"name": "text", 
                    "session_ids": "text", 
                    "session_titles": "text", 
                    "num_sessions": "text"}
    

    # value checking/changing - exiting program if user doesn't have the correct input
    if (column == "location"):
        value = value.capitalize()
        # print("calling it on this", value)
    elif (column == "title"):
        value = value.title()
    elif (column == "time_start") or (column == "time_end"):
        if value.find("AM") == -1 and value.find("PM") == -1:
            print("Please search for a date in the following format: \"HH:MM AM\" or \"HH:MM PM\"")
            sys.exit()
    elif (column == "date"):
        if value.find("'/'") == -1 or len(value) != 10:
            print("Please search for a date using the following format: \"MM/DD/YYYY\"")
            sys.exit()
    elif (column == "speaker"):
        if len(value.split(" ")) < 2:
            print("Please search for a speaker with both first and last name (and middle name if applicable) in the following format: \"First Last\"")
            sys.exit()
    elif (column == "description"):
        if value.find("\'") >= 0:
            value.replace("\'", "\'\'")

    # Calling lookup according to user parameters
    print("Calling lookup on query...")
    if (column == "speaker"):
        print("Opening speakers table instance...")
        speakers_table = db_table("Speakers", speaker_schema)
        sessions_list = speaker_query(value)
    else:
        sessions_list = lookup(sessions_table, column, value)

    # Taking all the valid sessions and printing them in a table format
    pretty_print(sessions_list)



    
    