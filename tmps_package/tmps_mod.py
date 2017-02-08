"""module tmps_mod containing classes"""

import os
import stat
import json 
import subprocess
import re

RACINE = os.path.join(os.path.sep,'tmp','tmps') # RACINE for all module (no choice!)
#os.path.sep is equal to '/' in linux

def tmps_error(a_text):
    """
    Prints error messages in standard format, and exit(1)
    """
    print "Error in tmps : {0} ; exit 1".format(a_text)
    exit(1)
    
class Tmps:
    """"Main classe. Manage Tmps objects for environment self.env.
    Tmps correspond to files in directory /tmp/tmps/<env>/.
    Manage means: list (get), create (post), update (put), delete (delete)
    
    Attributes:
        env   environment
        pk    primary key (correspond to the argument -k <pk>)
        name  name defined in json input file (pk and name must match)
    """
    
    def json_read(self, a_json):
        """Read json input and perform some checks.
        - mode must be 0[2,6,7][1-7]{2} (0644, 0755, 0632...)
        - name must be \w+"""
        parsed_json = json.loads(a_json)
        env = parsed_json['env']
        if (self.env != env):
            tmps_error("json_read: env " + self.env + "different from json env " + env)
        self.name = parsed_json['name']
        if (not re.match(r"^\w+$",self.name)):
            tmps_error("json_read: name is not \w+ :" + self.name)
        self.mode = parsed_json['mode']
        if (not re.match(r"^0[2,6,7][1-7]{2}$",self.mode)):
            tmps_error("json_read: mode is not 00[2,6,7][1-7]{2} :" + self.mode)
        
    def get_all(self):
        """List all tmps files from env."""
        my_list = ListOfTmpsFile(self.env)
        print my_list.json()
    
    def get(self, pk):
        """List pk file from env."""
        tmps_file = TmpsFile(self.env, pk)
        tmps_file.get()
        print tmps_file.json()

    def post(self, json):
        """Create tmps file, in environment env, from json."""
        self.json_read(json)
        tmps_file = TmpsFile(self.env, self.name)
        if (not tmps_file.check()):
            tmps_file.mode = self.mode
            tmps_file.save()
            print tmps_file.json()
        else:
            tmps_error("post: file stil exists " + self.name)

    def put(self, pk, json):
        """Update tmps file, identified by pk, in environment env, from json."""
        self.json_read(json)
        if (pk != self.name):
            tmps_error("put: pk " + pk + "different form name in json: " + self.name)
        tmps_file = TmpsFile(self.env, pk)
        if (tmps_file.check()):
            tmps_file.mode = self.mode
            tmps_file.save()
            print tmps_file.json()
        else:
            tmps_error("put: file does not exist " + pk)
    
    def delete(self, pk):
        """Delete a specific file, identified by pk."""
        tmps_file = TmpsFile(self.env, pk)
        if (tmps_file.check()):
            try:
                tmps_file.delete()
            except:
                tmps_error("delete: delete ko for file " + pk)
        else:
            tmps_error("delete: file does not exist " + pk)

    def __init__(self, env):
        """Tmps class constructor (need an env). 
        Create dir /tmp/tmps/<env> for all env if they don't exist.
        """
        self.env = env
        for my_env in ["dev","val","inf","fr"]:
            my_path = os.path.join(RACINE,my_env)
            if not os.path.exists(my_path):
                os.makedirs(my_path)


class ListOfTmpsFile:
    """ListOfTmpsFile: list of TmpsFile in directory <env>"""
     
    def json(self):
        """Return list of TmpsFile in json format"""
        return json.dumps(self.list_of_files, sort_keys=True, indent=4, separators=(',', ': '))

    def __init__(self, env):
        """ListOfTmpsFile class constructor. List files from directory <env>.
        List is a list of json descriptors."""
        self.list_of_files = list()
        racine = os.path.join(RACINE,env) 
        if (os.path.isdir(racine)):
            for file_name in os.listdir(racine):
                if os.path.isfile(os.path.join(racine,file_name)):
                    long_file_name = os.path.join(racine,file_name)
                    mode = oct(stat.S_IMODE(os.stat(long_file_name)[stat.ST_MODE])) #mode of the file
                    self.list_of_files.append({'env':env, 'name': file_name, 'mode': mode})
        else:
            tmps_error(self.__racine + ": no such dir.")

class TmpsFile:
    """TmpsFile: file TmpsFile, identified by env and pk
        
    Attributes:
        env   environment
        pk    primary key (correspond to the argument -k <pk>)
    """

   
    def json(self):
        """Return TmpsFile in json format."""
        j = ({'env':self.__env, 'name': self.__name, 'mode': self.mode})
        return json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))

    def save(self):
        """Create or update file."""
        try:
            open(self.__long_name, 'a').close() #create an empty file
            myPopen = subprocess.Popen(['chmod', self.mode, self.__long_name])
        except:
            tmps_error("Creation of file " + self.__name)

    def check(self):
        """Check if file exists and return True or False."""
        if os.path.isfile(self.__long_name):
            return True
        else:
            return False

    def get(self):
        """Get mode for file."""
        if os.path.isfile(self.__long_name):
            self.mode = oct(stat.S_IMODE(os.stat(self.__long_name)[stat.ST_MODE])) #mode of the file
        else:
            tmps_error("Get: non existing file " + self.__long_name)

    def delete(self):
        """Delete file."""
        if os.path.isfile(self.__long_name):
            try:
                os.remove(self.__long_name)
            except:
                tmps_error("Delete: file " + self.__long_name)
        else:
            tmps_error("Delete: non existing file " + self.__long_name)

    def __init__(self, env, name):
        """TmpsFile class constructor. Default mode is 0644.
        Other attributes (env, racine, name, long_name) cannot be modified."""
        self.__env = env
        racine = os.path.join(RACINE,self.__env) #internal attribute (AttributeError if accessed)
        self.__name = name
        #print "DEBUG: name={0}".format(name)
        self.__long_name = os.path.join(racine,self.__name)
        self.mode = "0644"
        
