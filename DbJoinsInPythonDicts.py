"""
I found that selecting a million records can typically be done in about 3 seconds, 
however JOINS may slow down the process. 

In this case that one has approximately 150k Foo's which has a 1-many relation to 1M Bars,
then selecting those using a JOIN may be slow as each Foo is returned approximately 6.5 
times. I found that selecting both tables seperately and joining them using dicts in 
python is approximately 3 times faster than SQLAlchemy (approx 25 sec) and 2 times faster 
than 'bare' python code using joins (approx 17 sec). 
 
The code took 8 sec in my use case. Selecting 1M records without relations, like the 
Bar-example above, took 3 seconds. I used this code:

Seen on StackOverflow:	https://stackoverflow.com/questions/23185319/why-is-loading-
						sqlalchemy-objects-via-the-orm-5-8x-slower-than-rows-via-a-raw-my
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import sys
import time
import datetime
import inspect
from operator import itemgetter, attrgetter

# fetch all objects of class Class, where the fields are determined as the
# arguments of the __init__ constructor (not flexible, but fairly simple ;))
def fetch(Class, cursor, tablename, ids=["id"], where=None):
    arguments = inspect.getargspec(Class.__init__).args; del arguments[0];
    fields = ", ".join(["`" + tablename + "`.`" + column + "`" for column in arguments])
    sql = "SELECT " + fields + " FROM `" + tablename + "`"
    if where != None: sql = sql + " WHERE " + where
    sql=sql+";"
    getId = itemgetter(*[arguments.index(x) for x in ids])
    elements = dict()

    cursor.execute(sql)
    for record in cursor:
        elements[getId(record)] = Class(*record)
    return elements

# attach the objects in dict2 to dict1, given a 1-many relation between both
def merge(dict1, fieldname, dict2, ids):
    idExtractor = attrgetter(*ids)
    for d in dict1: setattr(dict1[d], fieldname, list())
    for d in dict2:
        dd = dict2[d]
        getattr(dict1[idExtractor(dd)], fieldname).append(dd)

# attach dict2 objects to dict1 objects, given a 1-1 relation
def attach(dict1, fieldname, dict2, ids):
    idExtractor = attrgetter(*ids)
    for d in dict1: dd=dict1[d]; setattr(dd, fieldname, dict2[idExtractor(dd)])

