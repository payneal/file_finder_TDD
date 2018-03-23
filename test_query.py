import unittest
import os
from querySearch import QuerySearch

class Test_Query_Search(unittest.TestCase):

    def setUp(self):
        self.search = QuerySearch()

    def tearDown(self):
        pass

    def test_topics_when_none(self):
        topics = self.search.get_topics()
        self.assertEqual(topics, [])


    def test_adding_search_topick(self):
        self.search.add_topic(
            "POA", "Power of Attorney")
        self.search.add_topic(
            "QA", "Questionaire")
        topics = self.search.get_topics()
        self.assertEqual(topics, 
            [{   
                "abbreviation": "poa", 
                "name": "power of attorney"
            },{
                "abbreviation": "qa", 
                "name": "questionaire"
            }]
        )

    def test_add_to_directory_location(self): 
        self.search.add_to_location("search_folder")
        self.assertEqual(
            self.search.location, os.getcwd() + "/search_folder/")
        
    def test_find_person_not_there(self):
        x = self.search.find_using_topics("poa", "ali", "payne")
        self.assertEqual({}, x)

    def test_find_person_not_there_no_topics(self):
       x = self.search.find("yuyui", "ali", "payne")
       self.assertEqual({}, x)
      
    def test_find_person_not_there_with_idx(self):
        x = self.search.find_using_topics("poa", "ali", "payne", 1)
        self.assertEqual({}, x)

    def test_find_all_files_of_bad_user(self):
        x = self.search.find_all("Ali", "Payne");
        self.assertEqual({}, x)
    
    def test_find_all_files_of_bad_user_with_idx(self):
        x = self.search.find_all("Ali", "Payne", 1);
        self.assertEqual({}, x)

    def test_find_with_id_but_not_correct_file_search_name(self):
        self.search.add_to_location("search_folder")
        x = self.search.find("dob", "John", "Smith", 2)
        self.assertEqual({}, x)

    def test_find_with_id_file_search_name(self):
        self.search.add_to_location("search_folder")
        x = self.search.find("poa", "John", "Smith", 2)
        self.assertEqual(
            {'fileLocation':  "z:/Smith, John 2/POA - 2.pdf"}, x)

    def test_find_no_id_file_search_name(self):
        self.search.add_to_location("search_folder")
        x = self.search.find("Power of Attorney", "Rudy", "Gibson")
        self.assertEqual(
            {'fileLocation':  "z:/Gibson, Rudy/Power of Attorney.pdf"}, x)

    def test_find_with_id_using_find_with_topics(self):
        self.search.add_topic(
            "POA", "Power of Attorney")
        self.search.add_topic(
            "QA", "Questionaire")
        self.search.add_to_location("search_folder")
        x = self.search.find_using_topics("poa", "John", "Smith", 1)
        self.assertEqual(
            {'fileLocation':  "z:/Smith, John 1/Power of Attorney - 1.pdf"}, x)
   
    def test_find_with_no_id_only_one_entry(self):
        self.search.add_topic(
            "POA", "Power of Attorney")
        self.search.add_to_location("search_folder")
        x = self.search.find_using_topics("poa","Rudy", "Gibson")
        self.assertEqual(
            {'fileLocation':  "z:/Gibson, Rudy/Power of Attorney.pdf"}, x)

    def test_find_but_has_multiple_entries_with_topics(self):
        self.search.add_topic("POA", "Power of Attorney")
        self.search.add_to_location("search_folder")
        x = self.search.find_using_topics("poa","Susan", "Sanders")
        self.assertEqual({"ids": [1, 2]}, x)

    def test_find_but_has_multiple_entries(self):
        self.search.add_to_location("search_folder")
        x = self.search.find("poa","Susan", "Sanders")
        self.assertEqual({"ids": [1, 2]}, x)

    def test_find_file_but_altered_location(self):
        self.search.add_topic("POA", "Power of Attorney")
        self.search.add_to_location("search_folder")
        x = self.search.find_using_topics("poa", "Susan", "Sanders" , 1)

        self.assertEqual({
            'fileLocation': "z:/Sanders, Susan 1/Susan Sanders's Power of Attorney - 1.pdf"},x)

    def test_find_all_files_of_one_person_with_idx(self):
        self.search.add_topic("POA", "Power of Attorney")
        self.search.add_to_location("search_folder")
        x = self.search.find_all("John", "Smith", "1")
        self.assertEqual({
            "files":
                ["z:/Smith, John 1/Power of Attorney - 1.pdf"]},
            x)    
    
    def test_find_all_files_of_one_person_with_no_idx_but_not_multi(self):
        self.search.add_topic("POA", "Power of Attorney")
        self.search.add_to_location("search_folder")
        x = self.search.find_all("Rudy", "Gibson")
        self.assertEqual(
            {'files': ["z:/Gibson, Rudy/Power of Attorney.pdf"]}, x)

    def test_find_all_files_of_one_person_with_no_idx_but_multi(self):
        self.search.add_topic("POA", "Power of Attorney")
        self.search.add_to_location("search_folder")
        x = self.search.find_all("John", "Smith")
        self.assertEqual({"ids": [1, 2]}, x)

    def test_get_creation_date_for_file(self):
        umm = os.getcwd() + "/search_folder/Bobby, Ricky/Power of Attorney.pdf"
        x = self.search.get_creation_date(umm)
        self.assertEqual('2017-02-20 00:00:00', x)

    def test_get_all_files_with_creation_date(self):
        self.search.add_to_location("search_folder")
        x =  self.search.get_all_files_with_creation_date()
        expected_answer = {
            '/Users/alipayne/Desktop/upwork_stuff/JosephLancaster/folderapi/search_folder/Gibson, Rudy': {
                'dirnames': [],
                'created': {'Power of Attorney.pdf': '2018-03-10 21:03:57'}, 
                'filenames': ['.DS_Store', 'Power of Attorney.pdf']
            }, '/Users/alipayne/Desktop/upwork_stuff/JosephLancaster/folderapi/search_folder/Smith, John 1':{
                'dirnames': [], 
                'created': {'Power of Attorney - 1.pdf': '2018-03-10 21:03:57'}, 
                'filenames': ['.DS_Store', 'Power of Attorney - 1.pdf']
            }, '/Users/alipayne/Desktop/upwork_stuff/JosephLancaster/folderapi/search_folder/Smith, John 2': {
                'dirnames': [],
                'created': {'POA - 2.pdf': '2018-03-10 21:03:57'},
                'filenames': ['.DS_Store', 'POA - 2.pdf']
            }, '/Users/alipayne/Desktop/upwork_stuff/JosephLancaster/folderapi/search_folder/Bobby, Ricky': {
                'dirnames': [],
                'created': {'Power of Attorney.pdf': '2017-02-20 00:00:00'}, 
                'filenames': ['.DS_Store', 'Power of Attorney.pdf']
            }, '/Users/alipayne/Desktop/upwork_stuff/JosephLancaster/folderapi/search_folder/Sanders, Susan 2': {
                'dirnames': [],
                'created': {'Power of Attorney - 2.pdf': '2018-03-10 21:03:57'}, 
                'filenames': ['.DS_Store', 'Power of Attorney - 2.pdf']
            }, '/Users/alipayne/Desktop/upwork_stuff/JosephLancaster/folderapi/search_folder/Sanders, Susan 1': {
                'dirnames': [], 
                'created': {"Susan Sanders's Power of Attorney - 1.pdf": '2018-03-10 21:03:57'}, 
                'filenames': ['.DS_Store', "Susan Sanders's Power of Attorney - 1.pdf"]}}
        self.assertEqual(expected_answer, x)

    def test_find_all_due_files(self):
        self.search.add_topic("POA", "Power of Attorney")
        self.search.add_to_location("search_folder")
        x = self.search.due(90) 
        self.assertEqual({'files':  ["z:/Bobby, Ricky/Power of Attorney.pdf"]}, x)

    def test_find_all_due_files_with_type(self):
        self.search.add_to_location("search_folder")
        x = self.search.due(90, 'Power of Attorney')
        self.assertEqual({'files': ["z:/Bobby, Ricky/Power of Attorney.pdf"]}, x)

if __name__ == "__main__":
    unittest.main()
