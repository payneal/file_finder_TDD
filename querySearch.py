import os
import  platform
import time
import datetime
#cwd = os.getcwd()

class QuerySearch:
  
    def __init__(self):
        self.location =  None
        self.reset_location()
        self.topics = []
        # options = windows, mac, linux
        # cmake sure you change or you will get weird creatio dates
        self.os = "mac"

    def get_topics(self):
        return self.topics;

    def add_topic(self, abv, name):
        self.topics.append({
            "abbreviation": abv.lower(), 
            "name": name.lower()})

    def add_to_location(self, add_on):
        self.location += add_on + "/"

    def reset_location(self):
        self.location = os.getcwd() +"/" 

    def get_topics(self):
        return self.topics

    def find(self, file_type, first, last, idx=None):
        arg = self.__obtain_search_loc(last,first, idx)
        f,d = self.__get_files_and_dirs_level_one()
        return self.__search_for_find(f, d, arg, file_type, first, last, idx)
        
    def find_using_topics(self, file_type, first, last, idx=None): 
        search_loc = self.__obtain_search_loc(last, first, idx) 
        if not self.__check_if_found(search_loc):
            return self.__match_if_multis_found(file_type,search_loc, idx, first)
        return self.__match(search_loc, file_type, idx)

    def find_all(self, first, last, idx=None):
        files, dirs = self.__get_files_and_dirs_level_one()
        search_loc = self.__obtain_search_loc(last, first, idx) 
        return self.__find_last_first_all(files, dirs, search_loc)

    def due(self, days, file_type=None):
        info  = self.__get_all_files_with_creation_date()
        stuff_due = self.__get_due_info(days, file_type, info)
        return {'files': stuff_due}
            
    def get_creation_date(self, file_location):
        return self.__creation_date(file_location)

    def get_all_files_with_creation_date(self):
        return self.__get_all_files_with_creation_date()

    # private
    # --------------------------------------------------------------------
        
    def __get_due_info(self, days, file_type, info):
        stuff_due = []
        for dir_name in info:
            for f_name in info[dir_name]['created']:
                created_date = info[dir_name]['created'][f_name]
                datetime_obj = datetime.datetime.strptime(created_date,  "%Y-%m-%d  %H:%M:%S")
                current = datetime.datetime.today()
                days_passed = (current - datetime_obj).days
                self.__check_vs_due_date(days_passed, days, dir_name, file_type, f_name, stuff_due)
        return stuff_due

    def __check_vs_due_date(self, days_passed, days, dir_name, file_type, f_name, stuff_due):
        if days_passed >= days:
            name_dir = dir_name.rsplit("/", 1)
            if file_type:
                fname_to_compare = f_name.split(".")
                fname_to_compare= fname_to_compare[0]
                if file_type == fname_to_compare:
                    stuff_due.append("z:/{}/{}".format (name_dir[1], f_name))
            else:
                stuff_due.append("z:/{}/{}".format (name_dir[1], f_name))

    def __get_all_files_with_creation_date(self):
        info = self.__get_all_dirs_files({})
        for dir_name in info:
            for file_name in info[dir_name]['filenames']:
                if file_name[0] is not ".":
                    file_loc = "{}/{}".format(dir_name, file_name)
                    c_date = self.__creation_date(file_loc)
                    info[dir_name]["created"] = {}
                    info[dir_name]["created"][file_name] = c_date
        del info[self.location]
        return info
 
    def __creation_date(self, path_to_file):
        # take from https://stackoverflow.com/questions/237079/how-to-get-file-creation
        ts_epoch = None
        if self.os == "mac":
            stat = os.stat(path_to_file)
            ts_epoch = int(stat.st_birthtime)             
        elif self.os == "windows":
            # uses modification date
            ts_epoch = os.path.getctime(path_to_file)
        elif self.os == "linux":
            # uses modification date
            ts_epoch = os.stat(path_to_file).st_mtime 
        if ts_epoch:
            return datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
     
    def __search_for_find(self, files, dirs, arg, file_type, first, last, idx):
        stuff = {}
        ids = []
        for dir_name in dirs: 
            answer = self.__check_vs_dirname(dir_name, arg, stuff, file_type, ids)
            if type(answer) is dict:
                return answer   
        return self.__if_multiples_get_ids(ids)

    def __check_vs_dirname(self,dir_name, arg, stuff, file_type, ids):
        if dir_name == arg:
            return self.__check_within_dir( dir_name, arg, stuff, file_type)
        if arg in dir_name:
            ids.append(int(dir_name[len(dir_name)-1]))
            
    
    def __if_multiples_get_ids(self, umm):
        if len(umm) == 0:
            return {}
        else:
            return {"ids": umm}

    def __check_within_dir(self, dir_name, arg, stuff, file_type):
        arg = dir_name.split(", ")
        if len(arg[1].split(" ")) == 2:
            args = arg[1].split(" ")
            args.append(arg[0]) 
            return self.__locate_files_based_on_args(
                stuff, arg, file_type, dir_name, 2)
        else:
            return self.__locate_files_based_on_args(
                stuff, arg, file_type, dir_name, 1)

    def __locate_files_based_on_args(self,stuff,  arg, file_type, dir_name, option):
        stuff, location = self.__get_all_folder_info_with_location(stuff, arg)
        filenames = self.__located_file_match(location, stuff)  
        if filenames:
            return self.__check_folder_for_file(
                filenames, location, stuff, file_type, dir_name, option) 
        return {}

    def __located_file_match(self, location, stuff):
        if location in stuff:
            return stuff[location]['filenames']
        return False

    def __check_folder_for_file(self, filenames, location, stuff, file_type, dir_name, option):
        for file_name in filenames:
            the_split = file_name.split(" ")
            if (len(the_split) > 0 and option == 2):
                if the_split[0].lower() == file_type:
                    return self.__get_z_location(dir_name, file_name)
            elif option == 1:
                if file_type.lower() in file_name.lower():
                    return self.__get_z_location(dir_name, file_name)
        return {}

    def __get_z_location(self, dir_name, file_name):
        return {'fileLocation': "z:/{}/{}".format(dir_name, file_name)}
  
    def __get_all_folder_info_with_location(self, stuff, arg):
        return self.__get_all_dirs_files(stuff), self.location + arg[0] + ", "+ arg[1]
  
    def __get_all_dirs_files(self, stuff):
        f, d = [], []
        for (dirpath, dirnames, filenames) in os.walk(self.location):
            stuff[dirpath] = {}
            stuff[dirpath]['filenames'] = filenames
            stuff[dirpath]['dirnames'] = dirnames
        return stuff

    def __match_if_multis_found(self, file_type, search_loc, idx, first):
        multi = self.__get_multis(search_loc)
        if multi:
            return{"ids":multi}  
        else:   
            return {}

    def __get_multis(self, search_loc):
        idx = 1
        user_ids=[]
        while True:
            if os.path.isdir(self.location+search_loc+" {}".format(idx)):
                user_ids.append(idx)
                idx += 1
            elif idx == 1:
                return False
            else:
                return user_ids

    def __check_if_found(self, search_loc):  
        files, dirs = self.__get_files_and_dirs_level_one() 
        if self.__is_search_location_findable(search_loc, dirs):
            return True
        return False

    def __match(self, search_loc, file_type, idx):
        abv, name, potential_name = self.__obtain_abv_name_potential(
            search_loc,file_type, idx)
        f,d = self.__get_files_and_dirs_level_one(self.location + search_loc)    
        for x in range(0, len(f)):
            if self.__check_match(f, x, potential_name):
                return {"fileLocation": "z:/"+ search_loc +"/"+ f[x]}
        return "Error"

    def __check_match(self, f, x, potential_name):
        if f[x].lower() == potential_name or potential_name in f[x].lower():
            return True
        return False

    def __obtain_abv_name_potential(self, search_loc,file_type, idx):
        if idx:
            return self.__find_file_type_last_first_with_idx(search_loc, file_type, idx)  
        abv, name, potential_name = self.__find_file_type_last_first_info(file_type);
        potential_name += ".pdf"
        return abv, name, potential_name

    def __obtain_search_loc(self, last, first, idx):
        if idx:
            return self.__get_search_location_based_on_idx(last, first, idx)
        return self.__get_search_location(last, first)

    def __find_file_type_last_first_with_idx(self, search_loc, file_type, idx): 
        return self.__get_file_type_last_first_info_with_idx(file_type, idx)

    def __find_file_type_last_first(self, file_type, dirs, search_loc,idx, last, first):
        if self.__is_search_location_findable(search_loc, dirs):
            return self.__file_type_last_first(search_loc, file_type, last, first)
        return {}
   
    def __is_search_location_findable(self, search_loc, dirs): 
        if self.__check_if_in_search_location(search_loc, dirs):
            return True   
        return False

    def __find_file_type_last_first_info(self, file_type):
        abv, name = self.__get_abbrev(file_type)
        potential_name = name.lower() 
        return abv,name, potential_name 
      
    def __get_file_type_last_first_info_with_idx(self, file_type, idx):
        abv, name, potential_name = self.__find_file_type_last_first_info(file_type)
        return abv, name, potential_name+" - {}.pdf".format(idx)

    def __get_abbrev(self, file_type):
        for x in range(0, len(self.topics)):
            if self.topics[x]['abbreviation'] == file_type:
                return file_type, self.topics[x]['name']
        return False

    def __find_last_first_all(self, files, dirs, search_loc):
        if not self.__is_search_location_findable(search_loc, dirs):
            return self.__find_all_last_first_multi(search_loc)
        return self.__get_all_files_in_dir(search_loc)

    def __find_all_last_first_multi(self, search_loc):
        answer = self.__get_multis(search_loc)
        if answer:
            return {'ids': self.__get_multis(search_loc)}
        else:
            return {}

    def __get_all_files_in_dir(self, search_loc):
        f,d = self.__get_files_and_dirs_level_one(self.location + search_loc)    
        all_files = [] 
        for x in f:
            if x[0] is not ".":
                all_files.append("z:/"+ search_loc +"/"+ x)
        return {'files': all_files}
     
    def __check_if_in_search_location(self, search_loc, dirs):
        answer= False
        for x in dirs:  
            if x == search_loc:
                return True;
        return False
     
    def __get_search_location(self, last, first):
        return "{}".format(last+", "+first)  
     
    def __get_search_location_based_on_idx(self, last, first, idx):
        return self.__get_search_location(last, first) + " {}".format(idx)
    
    def __get_files_and_dirs_level_one(self, location=None):
        if not location:
            location = self.location
        f, d = [], []
	for (dirpath, dirnames, filenames) in os.walk(location):
    		f.extend(filenames)
		d.extend(dirnames)
		break
	return f, d
