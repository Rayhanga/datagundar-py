from proxy import OpenWeb

from definitions import DATA_DIR
import datamanager

import os
import re

def getCourseList(proxy):
    result = []

    courseSauce = proxy.getSauce(expectedClassName='list-group-item course-listitem')
    courseList = courseSauce.findAll('li', {'class': 'course-listitem'})

    for course in courseList:
        courseItem = course.find('a', {'class': 'coursename'})

        try:
            courseProgress = course.find('strong').text
        except:
            courseProgress = None

        courseData = courseItem.text.replace('Course name', '').replace('Course is starred', '').replace('\n', '').split('|')
        courseData = [re.sub(r"(\W{2,})|(^\W)|(\W$)", "", t) for t in courseData]

        courseId = courseItem.attrs.get('href')[-4:]
        courseTahunAjar = courseData[0]
        courseKelas = courseData[1]
        courseTitle = courseData[2]
        courseDosen = courseData[3].title()

        result.append({
            'courseID': courseId,
            'courseTitle': courseTitle,
            'courseKelas': courseKelas,
            'courseDosen': courseDosen,
            'courseTahunAjar': courseTahunAjar,
            'courseTopics': []
        })

    return result

def getCourseDetails(proxy, course):
    result = []

    proxy.openPage(proxy.website['COURSE'](course['courseID']))
    topicSauce = proxy.getSauce(expectedClassName='main')
    topicList = topicSauce.findAll('li', {'class': 'section main clearfix'})

    for topicItem in topicList:
        topicId = course['courseID'] + '#' + topicItem.attrs.get('id')
        topicTitle = topicItem.attrs.get('aria-label')
        activityList = topicItem.findChildren('li', {'class': 'activity'})

        topicActivities = []

        for activityItem in activityList:
            activityLink = activityItem.find('a').attrs.get('href').replace('https://','').split('/')
            activitySpan = activityItem.find('span', {'class': 'instancename'})
            activityAccesshide = activitySpan.find('span', {'class': 'accesshide'})
            activityId = activityLink[3].replace('view.php?id=', '')
            activityType = activityLink[2]
            if activityAccesshide:
                activityTitle = re.sub(r"(^\W)", "", activitySpan.text).replace(activityAccesshide.text, "")
            else:
                activityTitle = re.sub(r"(^\W)", "", activitySpan.text)

            if 'materi' in activityTitle.lower():
                activityType = 'resource'

            if activityItem.find('img', {'class': 'icon'}):
                if 'Completed' in activityItem.find('img', {'class': 'icon'}).attrs.get('alt'):
                    activityCompleted = True
                elif 'Not completed' in activityItem.find('img', {'class': 'icon'}).attrs.get('alt'):
                    activityCompleted = False
            else:
                activityCompleted = None

            topicActivities.append({
                'activityID': activityId,
                'activityTitle': activityTitle,
                'activityType': activityType,
                'activityCompleted': activityCompleted
            })

        result.append({
            'topicID': topicId,
            'topicTitle': topicTitle,
            'topicActivities': topicActivities
        })
        
    course['courseTopics'] = result

    return course

def getCourseData(credentials):
    with OpenWeb(
        website={
            'MAIN': 'https://v-class.gunadarma.ac.id/my/',
            'LOGIN': 'https://v-class.gunadarma.ac.id/login/index.php',
            'COURSE': lambda courseId : 'https://v-class.gunadarma.ac.id/course/view.php?id={}'.format(courseId),
            'ACTIVITY': lambda activityType, activityId : 'https://v-class.gunadarma.ac.id/mod/{}/view.php?id={}'.format(activityType, activityId)
        },
        credentials={
            'username': credentials.username,
            'password': credentials.password
        },
        headless=True
    ) as vclassProxy:
        courseList = getCourseList(vclassProxy)
        for course in courseList:
            getCourseDetails(vclassProxy, course)
            
        return courseList

# def getTopicDetails(proxy, topic):
#     for activity in topic['topicActivities']:
#         if activity['activityType'] in ["quiz", "assign", "forum"]:
#             proxy.openPage(proxy.website['ACTIVITY'](activity['activityType'], activity['activityID']))
#             activitySauce = proxy.getSauce(expectedXpath="//*[@role='main']")
#             activityDataContainer = activitySauce.find('div', {'role': 'main'})
#             activityDescriptionContainer = activityDataContainer.find('div', {'id': 'intro'})
#             activityDescriptions = activityDescriptionContainer.findAll('div') if activityDescriptionContainer else None

#             activityInfo = None
#             activityFeedback = None

#             if activity['activityType'] == "quiz":
#                 activityInfo = [info.text for info in activityDataContainer.find('div', {'class': 'quizinfo'}).findAll('p')]
#                 activityFeedbackContainer = activityDataContainer.find('table', {'class': 'quizattemptsummary'})
#                 activityFeedback = activityFeedbackContainer.findAll('tr') if activityFeedbackContainer else None
#             elif activity['activityType'] == "assign":
#                 activityData = [info.text for info in activityDataContainer.find('table', {'class': 'generaltable'}).findall('td')][:-1]
#                 activityInfo = activityData[2:]
#                 activityFeedback = activityData[:2]
#             elif activity['activityType'] == "forum":
#                 pass
#                 # activitySauce = vclassProxy.getSauce(expectedClassName='discussion-list')
#             else:
#                 logging.warning('%s as %s is unhandled', activity['activityID'], activity['activityType'])

#             activity['activityInfo'] = activityInfo
#             activity['activityFeedback'] = activityFeedback
#         elif activity['activityType'] == "url":
#             # TODO: Download URL
#             pass
#         elif activity['activityType'] == "resource":
#             # TODO: Download resource
#             pass
#         else:
#             logging.warning('%s as %s is unhandled', activity['activityID'], activity['activityType'])    

#     return topic