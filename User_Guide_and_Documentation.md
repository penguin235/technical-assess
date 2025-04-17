DOCUMENTATION

# User and Developer Guide 

# How to Run Program
1. cd into AgendaImport. 
2. Create a virtual environment in repository and activate.
3. Install requirements on command line using: pip install -r requirements.txt
4. Call import: $ python import_agenda.py <xls.input>
5. Call lookup: $ python lookup_agenda.py <column> <value>
    - If your input format resulted in program termination or unexpected results, please refer to the error message or the "Calling Lookup" sections below.


# Calling Lookups

**Date**: 
- $ python lookup_agenda.py date MM/DD/YYYY
- $ python lookup_agenda.py date "MM/DD/YYYY"
- ex: $ python lookup_agenda.py date 06/16/2018

**Time_Start or Time_End**: 
- $ python lookup_agenda.py time_start "HH:TT AM/PM"
- $ python lookup_agenda.py time_end "HH:TT AM/PM"
- ex: $ python lookup_agenda.py time_start "08:30 AM"
- ex: $ python lookup_agenda.py time_end "10:00 AM"

**Session Title**: 
- $ python lookup_agenda.py title "Complete Session Title"
- ex: $ python lookup_agenda.py title "Session 1A: Data centers"

**Location**: 
- $ python lookup_agenda.py location "Complete Location"
- $ python lookup_agenda.py location one_word_location
- ex: $ python lookup_agenda.py location Lobby
- ex: $ python lookup_agenda.py location "Coral Lounge"

**Description**: 
- $ python lookup_agenda.py description "Complete Description"

**Speakers**: (not attempted)
-  $ python lookup_agenda.py speaker "First Name"
- ex: $ python lookup_agenda.py speaker "Guruduth Banavar"
- Speaker: Tim Harris not getting processed

# Developer Documentation

**import_agenda.py:**
main:
- addresses command line inputs
- contains schema for sessions and speakers table
- deletes existing instance of interview_db
- creates instances of `db_table` for sessions and speakers
- calls `parse_store_excel`

'create_df'
Inputs: @param: excel file name
Ouputs: error if there is an issue, df if not issue
Function:
    - opens excel file
    - puts excel information into a df
    - returns dataframe

'store_db'
Inputs: @param: dataframe of an excel instance, db_instance
Ouputs: error if there is an issue
Function: puts df into a db
    - extracts row from df, puts into a dict object
    - cleans data
    - inserts speakers into speakers table
    - identifies session, subsession relationship
    - inserts sessions into sessions table

'parse_store_excel'
Inputs: @param: excel file (str), sessions table (db_table)
Ouputs: error if there is an issue
Function: 
    - calls create df to create a dataframe of the excel sheet
    - calls store db to store the dataframe into the sessions table

**'lookup_agenda.py'**

main:
- addresses command line inputs
- contains schema for sessions and speakers table
- creates instances of `db_table` for sessions and speakers
- calls `speaker_query` or `lookup` depending on input type

'lookup'
Input: @param: sessions_table, column, value
Output: array of all sessions and subsessions that match the query value
Function:
    - Extracts sessions and subsessions that directly match the parameter
    - Goes through the sessions and extracts associated subsessions

'speaker_query'
Input: @param: speaker
Output: Error if it is a certain speaker
Function:
    - does a query on the speakers table to identify what sessions the speaker is associated
    - calls lookup on all the sessions the speaker is associcated with

'pretty_print':
Input: @params: lookup_return array
Output: pretty printed output of query
Function:
    - only prints out spreadsheet information. nothing about the id of session
    - uses spacing and indenting for a cleaner output



# AI Usage
- I utilized ChatGPT when facing issues with debugging or syntax for a long period of time. My research order for debuggin were Whova provided resources, then Google search, and then AI.
- The only explicitly AI generated code were modifications to the SQL wrapper, specifically in the select function. I found that query parameters with apostrophes did not work with the exising implementation. I can drop a link to my ChatGPT session if necessary. 

# Process and Timeline
1) Thursday (4/10) - Saturday (4/12): 
    - Function structures and layout of project
2) (Sunday (4/13) - Monday (4/14)): 
    - Gained familiarity with SQL wrapper
    - Built a preliminary working script on import and lookup
3) (Monday (4/14) - Tuesday (4/15)): 
    - Experienced syntax and formatting issues
    - Started documentation
4) Wednesday (4/16):
    - Resolved a majority of issues experienced on Tuesday
    - Began refinement of features and solving niche/stretch bugs
    - Testing on command line
5) Thursday (4/17)
    - Refining features including querying and output
    - Added error handling
    - Continued testing on command line
    - Finalizing documentation


**Notes**
- If a field is empty, I swapped it out with "None Present"
- I was unable to perform a search query for Tim Harris. 
- At moment, I do not have a testing suite. I tested on command line. For future development, I would ideally create a testing suite for imports and lookups. 
- Can also use python3 instead of python

**Tests**
- PyUnit framework used for some mild testing

**Future Plan**
- resolve the Tim Harris speaker issue
- find an alternative implementation for select that does not modify existing implementation
- add more unit testing, especially for invalid inputs
