#!/usr/bin/python

#-*- coding: utf-8 -*-

import os, stat, json, re
import argparse
from tmps_package.tmps_mod import *

parser = argparse.ArgumentParser(description=
    """
    List, create, update or delete files in /tmp/tmps/<env> directory.
    """,
                                 epilog=
    """
    Environment is mandatory. It corresponds to dev, val, inf or fr.
   
    Actions are:
       * get: lists files (output=json file)
          * if PK (primary key, corresponding to the name of the file) is given:
            list the file
          * without PK : all files are listed
       * post: creates a new file (input=json file) - the name of the file is 
               provided in the json file
       * put: updates an existing file (input=json file) - the name of the file
              is provided in the json file
       * delete: deletes an existing file - the name of the file (PK) is set 
                 with '-k' option
   
    Json file format is the following:
       
        {
          "env": "<env>",
          "mode": "0<nnn>",
          "name": "<name>"
        },

    where:
       * <env> is the environment (must correspond to environment set with '-e'
         option)
       * <nnn> is the mode of the file, must respect regex "[2,6,7][1-7]{2}" 
         (examples: 0644, 0755, 0632...)
       * <name> is the name of the file (must respect regex "\w+")
    
    #Examples:
        
        tmps.py -e dev -a post \\
                -j '{"env":"dev","mode": "0644","name": "Maurice"}' 
    creates file Maurice, with mode "0644", for environment dev. File created is
    `/tmp/tmps/dev/Maurice`
        
        tmps.py -e dev -a get 
    lists files in `/tmp/tmps/dev`
        
        tmps.py -e dev -a put \\ 
                -j '{"env":"dev","mode": "0755","name": "Maurice"}' \\
                -k Maurice 
    updates file Maurice, with mode "0755", for environment dev.
        
        tmps.py -e dev -a get -k Maurice
    lists file  `/tmp/tmps/dev/Maurice`
        
        tmps.py -e dev -a delete -k Jean
    deletes file Maurice
    """,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("-e", "--env", required=True, 
                    choices=["dev", "inf", "val", "fr"], 
                    help="environment (limited to dev, inf, val and fr)")
                    # mandatory arguments
parser.add_argument("-a", "--action", required=True, 
                    choices=["get", "post", "delete", "put"], 
                    help="action to perform") 
                    # optional argument where possible values are limited
parser.add_argument("-j", "--json", help="json content") # optional argument
parser.add_argument("-k", "--pk", help="primary key (name of the file)") 
                    # optional argument

if __name__ == '__main__':
    args = parser.parse_args() # arguments are parsed

    #Check args
    if (args.action == "get"):
        if (args.json):
            tmps_error("Args check: get method: must not have json")
    elif (args.action == "post"):
            if (not args.json or args.pk):
                err_mess = "Args check: post method:"
                if (not args.json):
                    err_mess = " need json file"
                if (args.pk):
                    err_mess = err_mess + " must not have pk"
                tmps_error(err_mess)
    elif (args.action == "put"):
            if (not args.json or not args.pk):
                err_mess = "Args check: put method:"
                if (not args.json):
                    err_mess = " need json file"
                if (not args.pk):
                    err_mess = err_mess + " need pk"
                tmps_error(err_mess)
    elif (args.action == "delete"):
            if (args.json or not args.pk):
                err_mess = "Args check: delete method: "
                if (args.json):
                    err_mess = " must not have json"
                if (not args.pk):
                    err_mess = err_mess + " need pk"
                tmps_error(err_mess)
    
    #Let'go. Checks are ok.
    tmps = Tmps(args.env)
    if (args.action == "get"):
        if (args.pk):
            tmps.get(args.pk)
        else:
            tmps.get_all()
    elif (args.action == "post"):  
        tmps.post(args.json)
    elif (args.action == "put"):
        tmps.put(args.pk, args.json)
    elif (args.action == "delete"):
        tmps.delete(args.pk)
