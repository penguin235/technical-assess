from types import NoneType
from db_table import db_table
import pandas as pd
import argparse
import sys
import tabulate

def lookup(sessions_table, column, value):

    """
    Refinements/Task List:
    - PRIMARY FUNCTION: parameters: make value case-sensitive, type-safe (just can also give users a guide)
        - (Completed): case - all lower, all upper, capitalized
        - TODO: run query on multiple speakers
        - Cimpleted: run query on descriptions with apostrophe's
        - Dependency: import_agenda.py - determine query value
        - (complete): handled 1+ word arguments in main. directed user to use quotations
    - (unclear goal) CLEANUP: clean up return values of items (if possible)
    - STRETCH: try to go session, subsession, rather than sessions -> subsession
        - Dependency: pretty_print
    """

    print("Retrieving all sessions and subsessions that match lookup parameters...\n")

    # performing lookup on all sessions and subsession
    # retrieving all values instead of just a select few

    # improving case sensitivity

    standard_return = sessions_table.select(['id', 'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker', 'parent', 'parent_title'], {column: value})
    print("Extracted", len(standard_return), "sessions and subsessions that match this parameter.\n")

    """
    # parse through for speakers, etc. just to make sure information is accurate
    for i in standard_return:
        print("ID:", i["id"], " | Title:", i["title"], " | Parent:", i["parent"])
    print()
    """
    
    print("Retrieving subsessions of selected sessions...\n")
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

def speaker_query(speaker):

    # error handling
    if (speaker =="Tim Harris"):
        print("Unable to process request, please try with another speaker.")
        sys.exit()
    
    standard_return = speakers_table.select(['name', 'session_ids', 'session_titles', 'num_sessions'], {"name": speaker})
    # getting all the sessions that this speaker is in
    if (len(standard_return) == 0):
        print("No sessions found for this speaker.")
        return []
    speaker_sessions = standard_return[0]["session_titles"].split(";")
    # prepping the array that will get returned
    return_array = []
    for s in speaker_sessions:
        print("Calling internal lookup on this session the speaker is involved in:", s, "\n")
        return_array += lookup(sessions_table, "title", s)

    return return_array

def pretty_print(lookup_return):

    """
    Refinement/Tasks:
    - PRIMARY FUNCTION: improve table view (cutting off large returns, aligning columns), and possibly add an extended list
    - PRIMARY FUNCTION: automate printing as much as possible (rather than individual if statements)
        - Dependency: table view within pretty pring
    - STRETCH: prompt to ask to see extended few of an entry that has been cutoff
    - (Completed) PRIMARY FUNCTION: type checking in return values (NaN, String)
        - (Complete) DEPENDENCY: lookup function - altering what gets returned from look up
        - (Completed) DEPENDENCY: import_agenda.py
    """
    print("Pretty printing the lookup values...\n")
    print("Creating chart/table...\n")

    # what to print: Title, Location, Description, Session/Subsession of What

    # returned values: 'id', 'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker', 'parent', 'parent_title']
    # printed values:  'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker'
    tabulate_table = []
    for i in lookup_return:
        # print("processing this item right now: ", i)
        entry = []

        entry.append(i["date"])
        entry.append(i["time_start"])
        entry.append(i["time_end"])

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
        
        entry.append(i["speaker"])


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
    print("Opening sessions table instance....\n")
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
    print("Calling lookup on query...\n")
    if (column == "speaker"):
        print("Opening speakers table instance...\n")
        speakers_table = db_table("Speakers", speaker_schema)
        sessions_list = speaker_query(value)
    else:
        sessions_list = lookup(sessions_table, column, value)

    # Taking all the valid sessions and printing them in a table format
    pretty_print(sessions_list)



    
    