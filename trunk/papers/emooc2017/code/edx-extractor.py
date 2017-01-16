'''
Created on Jan 8, 2016

@author: chema
'''
import json
import feedparser
import pandas as pd
import urllib2
from tweetpy.twitter import Twitter

SHAREDCOUNT_API_KEY = '<PUT_YOUR_KEY>'

def format(s):
    return "\""+s+"\","

def get_social_metrics(url, api_key):
    sharedcount_response = urllib2.urlopen('https://free.sharedcount.com/?url=' + url + '&apikey=' + api_key)
    return json.load(sharedcount_response)

if __name__ == '__main__':
    filecsv = open("edx-dump.csv", 'w')
    feed = feedparser.parse(r'EDX-DUMP-13012017.xml')
    courses = {}
    twitter = 0
    facebook = 0
    linkedin = 0
    for course in feed['entries']:
         course_url=course['link']
         social_metrics =  get_social_metrics(course_url, SHAREDCOUNT_API_KEY)
         try:
                  twitter = social_metrics['Twitter']
                  facebook = social_metrics['LinkedIn']
                  linkedin = social_metrics['Facebook']['total_count']
         except (RuntimeError, TypeError, NameError):
                  twitter = 0
                  facebook = 0
                  linkedin = 0
         print "Writing to file info of: "+course_url 
         filecsv.write((format(course['title']) + format(course['link']) + format(course['course_school'])+ format(course['id']) + format(str(twitter)) + format(str(linkedin)) + format(str(facebook))).encode("utf-8")+"\n")
    filecsv.close()