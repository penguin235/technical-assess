import unittest
import import_agenda
import lookup_agenda
from db_table import db_table
import os


class TestAgendaMethods(unittest.TestCase):

    def test_parse_store_db(self):
        if os.path.exists("interview_test.db"):
            os.remove("interview_test.db")
        session_schema = {"ID": "integer PRIMARY KEY", "date": "text", "time_start": "text", 
                      "time_end": "text", "title": "text", "location": "text",
                      "description": "text", "speaker": "text", "parent": "text", "parent_title": "text"}    
        sessions_table = db_table("Sessions", session_schema)
        speaker_schema = {"name": "text", 
                    "session_ids": "text", 
                    "session_titles": "text", 
                    "num_sessions": "text"}
        speakers_table = db_table("Speakers", speaker_schema)
        import_agenda.parse_store_excel("agenda.xls", sessions_table, speakers_table)
        testing_array = sessions_table.select(['ID'])
        print("Value of testing array: ", testing_array[-1]["ID"])
        self.assertEqual(len(testing_array) - 1, 63)
    
    def test_lookup_time_start(self):
        session_schema = {"ID": "integer PRIMARY KEY", "date": "text", "time_start": "text", 
                      "time_end": "text", "title": "text", "location": "text",
                      "description": "text", "speaker": "text", "parent": "text", "parent_title": "text"}    
        sessions_table = db_table("Sessions", session_schema)
        testing_array = lookup_agenda.lookup(sessions_table, "time_start", "08:30 AM")
        print("Value of testing array: ", len(testing_array))
        self.assertEqual(len(testing_array), 3)

    def test_lookup_location(self):
        session_schema = {"ID": "integer PRIMARY KEY", "date": "text", "time_start": "text", 
                      "time_end": "text", "title": "text", "location": "text",
                      "description": "text", "speaker": "text", "parent": "text", "parent_title": "text"}    
        sessions_table = db_table("Sessions", session_schema)
        testing_array = lookup_agenda.lookup(sessions_table, "location", "Room 300")
        print("Value of testing array: ", len(testing_array))
        self.assertEqual(len(testing_array), 21)
    
    

    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAgendaMethods('test_parse_store_db'))
    suite.addTest(TestAgendaMethods('test_lookup_time_start'))
    suite.addTest(TestAgendaMethods('test_lookup_location'))
    return suite



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
