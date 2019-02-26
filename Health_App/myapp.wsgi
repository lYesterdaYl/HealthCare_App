#!/usr/bin/python3.6
import sys
sys.path.insert(0,"/var/www/Health_App/")
sys.path.insert(0,"/var/www/Health_App/health_app/")
from health_app import app as application

application.secret_key = "secret_key"