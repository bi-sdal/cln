#!/usr/bin/env python
import os
import sys
import environ



if __name__ == "__main__":

    root = environ.Path(__file__) - 1
    env = environ.Env()
    env.read_env(root('.env'))    

    env('DJANGO_SETTINGS_MODULE', default="sdal_cln.settings.dev")    
    
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sdal_cln.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
