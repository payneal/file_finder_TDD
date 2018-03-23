# Search Query How to:

## setup
* python 2.7
* make sure you have pip installed an virtualenv
* start virtualenv: virtualenv venv
* start enviroment: source venv/bin/activate
* install req's: pip install requirements.txt
* look at documentation below to use

## adding a search describtion
* made this because wasnt sure about search query(etc.)
* file will always contain one version of the file description that we seek: POA (Power of Attorney), QA (Questionnaire), Agreement, Addendum, etc.
* check out folder structure of ./search_folder against test

```python
from querySearch import QuerySearch

search = querySearch()

## adding search topics.
search.add_topic("POA", "Power of Attorney")
search.add_topic("QA", "Questionaire")
#search.add_topic("ID", "Identification")

## viewing searchable first level files
x = seach.get_topics()
print x = "[
    {   
        abbreviation: "poa", 
        name: "power of attorney"
    },{
        abbreviation: "qa", 
        name: "questionaire"
    }
]"

## locating of poa but person not found
x = seach.find("poa","ali", "payne")
print x ="{}"

## location all files bad person
x = search.find_all("ali", "payne") 
print x = "{}" 

## find poa of Jonh smith using topics 
x = seach.find_using_topics("poa","John", "Smith", 1)
print x = { 
    fileLocation:  "z:/Smith,John1/PowerofAttorney-1.pdf"}

## find poa of John Smith with id
x = seach.find("poa","John", "Smith", 1)
print x = { 
    fileLocation:  "z:/Smith,John1/PowerofAttorney-1.pdf"}

## locating poa of Rudy Gibson no id only one entry
x = seach.find("poa","Rudy", "Gibson")
print x = {
    fileLocation:  "z:/Gibson, Rudy 1/Power of Attorney - 1.pdf"}

## locating of poa of Susan Sanders no id multiple 
x = seach.find("poa","Susan", "Sanders")
print x = "{ids:[1,2]}"

##  locating of file type but file location altered with file type name
x = search.find("poa", "Susan", "Sanders" , 1)
print x = {
    fileLocation:  "z:/Sanders, Susan 1/Susan Sanders's Power of Attorney - 1.pdf"}

## locate all files of Ruby Gibson
x = search.find_all("Ruby", "Gibson")
print x = "{ 
    fileLocations:[ "z:/Ruby, Gibson 1/Ruby Gibson's PowerofAttorney - 1.pdf"]}" 

## get creation date fo file
file_local = os.get_cwd + "Bobby, Ricky/Power of Attorney.pdf"
x = search.get_creation_date(file_local)
print x = "2017-2-20 00:00:00"

## get all file wit creation date
x = search.get_all_files_with_creation_date()
print  = {
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


## find all files date is later than 90 days ago.
x = search.find_due(90)
print x =  "{ 
    fileLocations:[ "z:/Bobby, Ricky/Power of Attorney.pdf"]}" 
```

## find all filename contains "Power of Attorney" AND date is later than 90 days ago.
x = search.find_due(90, "Power of Attorney")
print x =  "{ 
    fileLocations:[ "z:/Bobby, Ricky/Power of Attorney.pdf"]}" 
```

## How I altered the file creation date for my test
* http://blog.grapii.com/2010/07/change-a-files-creationmodified-date-on-mac-os-x/
* https://www.youtube.com/watch?v=CNCw0nVbBIk

* on mac example cli to change file date
``` bash
SetFile -d '02/20/2017 00:00:00' /file/flocation
```

* how t check for file creation date
* https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
* https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python

* how t check for file creation date
* https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
