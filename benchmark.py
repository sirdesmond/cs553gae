#!/usr/bin/python2
#import httplib
import requests
import json
import urllib
import os

testfiledir = './files'

files = os.listdir(testfiledir)

#conn = httplib.HTTPConnection("cs536storageproject.appspot.com")
url = 'http://cs536storageproject.appspot.com'
#url = 'http://localhost:8080'

total_insert_time = 0
total_get_time = 0
total_remove_time = 0
total_size = 0
headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}

import timeit
for i in [1,2]:
    # insert all
    for f in files:
        path= testfiledir + '/' + f
        total_size += os.path.getsize(path)
        args = {
                'filename': f,
                'submit' : 'submit'
                }
        s = timeit.timeit()
        r = requests.post(url+'/upload', data=args,
                files={'fileToUpload': open(path)})
        e = timeit.timeit()
        total_insert_time += e-s

    print "insert",i,"done"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # test Access

    for f in files:
        args = {
                'name': f
                }
        s = timeit.timeit()
        requests.get(url + '/read', params=args)
        e = timeit.timeit()
        total_get_time = e-s
    print "lookup",i,"done"


    for f in files:
        args = {
                'name': f
                }
        s = timeit.timeit()
        r = requests.get(url + '/delete' , params=args)
        e = timeit.timeit()
        total_remove_time += e-s
    print "remove",i,"done"

print "insert,",total_insert_time / total_size
print "lookup,",total_get_time / total_size
print "remove,",total_remove_time / total_size
print total_size
