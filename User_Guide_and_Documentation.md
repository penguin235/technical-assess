DOCUMENTATION

# User and Developer Guide 

# How to Run Program
1. cd into AgendaImport. 
2. Create a virtual environment in repository and activate.
3. Install requirements on command line using: pip -r install requirements.txt
4. Call import: $ python import_agenda.py <xls.input>
    - May need remove interview_test.db instance if making modifications to import. 
5. Call lookup: $ python lookup_agenda.py <column> <value>
    - If your input format resulted in program termination or unexpected results, please refer to the error message or the "Calling Lookup" sections below.


# Calling Lookups

**Date**: 
- $ python lookup_agenda.py date MM/DD/YYYY
- $ python lookup_agenda.py date "MM/DD/YYYY"
- ex: $ python lookup_agenda.py date 06/16/2018

**Time_Start or Time_End**: (Not working)
- $ python lookup_agenda.py time "HH:TT AM/PM"
- ex: $ python lookup_agenda.py time "08:30 AM"

**Session Title**: (Case Sensitivity)
- $ python lookup_agenda.py title "Complete Session Title"
- ex: $ python lookup_agenda.py title "Session 1A: Data centers"

**Location**: (Case Sensitivity)
- $ python lookup_agenda.py location "Complete Location"
- $ python lookup_agenda.py location one_word_location
- ex: $ python lookup_agenda.py location Lobby
- ex: $ python lookup_agenda.py location "Coral Lounge"

**Description**: (Not working for ')
- $ python lookup_agenda.py description "Complete Description"

**Speakers**: (not attempted)
- Tim Harris not getting processed

# Developer Documentation

**import_agenda.py:**
Main:



**lookup_agenda.py**

Main:
- does error handling for inputs and prompts user on the correct format





# AI Usage
- I utilized ChatGPT when facing issues with debugging or syntax. 
- The only explicitly AI generated code were modifications to the SQL wrapper, specifically in the select function. I found that query parameters with apostrophes did not work with the exising implementation. I can drop a link to my ChatGPT session if necessary. 

# Process

**Notes**
- If a field is empty, I swapped it out with 