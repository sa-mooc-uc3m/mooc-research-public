'''
Created on Jan 8, 2016

@see https://www.udemy.com/user/edit-api-clients/
@author: chema
'''

import json
import urllib
import pandas as pd

SHAREDCOUNT_API_KEY = '<PUT_YOUR_KEY>'
    
def main():
    response = urllib.urlopen('https://udacity.com/public-api/v0/courses')
    json_response = json.loads(response.read())
    courses_df = pd.DataFrame()
    course_data = json_response['courses']
    courses_df['title'] =  map(lambda course_data: course_data['title'], course_data)
    courses_df['homepage'] = map(lambda course_data: course_data['homepage'], course_data)
        
            #Getting Social Shares Data
    print 'Getting Social Shares Data'
    courses_df['course_url'] = 'https://www.coursera.org/course/' + courses_df['course_short_name']
    courses_df['sharedcount_metrics'] = map(lambda course_url: get_social_metrics(course_url, SHAREDCOUNT_API_KEY), courses_df['course_url'])
# 
    courses_df['twitter_count'] = map(lambda sharedcount: sharedcount['Twitter'], courses_df['sharedcount_metrics'])
    courses_df['linkedin_count'] = map(lambda sharedcount: sharedcount['LinkedIn'], courses_df['sharedcount_metrics'])
    courses_df['facebook_count'] = map(lambda sharedcount: sharedcount['Facebook']['total_count'], courses_df['sharedcount_metrics'])

    print 'Saving the Data'
    courses_df.to_csv('udacity_dump.tsv', sep='\t', encoding='utf-8')
if __name__ == '__main__':
    main()
