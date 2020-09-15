from datagundar.utils.proxy import Proxy
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime

site = {
    'LOGIN':'https://v-class.gunadarma.ac.id/login/index.php',
    'CALENDAR':'https://v-class.gunadarma.ac.id/calendar/view.php',
    'DASHBOARD':'https://v-class.gunadarma.ac.id/my/',
    'COURSE':'https://v-class.gunadarma.ac.id/course/view.php'
}

class Vclass(Proxy):
    def __init__(self, site=site):
        super().__init__(site)

    def filterCourseName(self, course_name):
        # Filter course name
        ## Soft filter
        softFilter = course_name.replace('Course name', '').replace('Course is starred', '').replace(' ','').replace('\n', '')
        ## Hard filter
        string = list(softFilter)
        temp = []
        c = 0
        for i in range(len(string)):
            if string[i] == '|':
                c += 1
            if c < 3 and c > 1:
                temp.append(string[i])
        ### Append some blank spaces
        string = ''.join(temp).replace('|', '').replace('(*)','').replace('#', '').replace('/','')
        temp = []
        for i in range(len(string)):
            if (string[i].isupper() or string[i].isdigit()) and i != 0:
                temp.append(' ')
            try:
                if string[i]+string[i+1]+string[i+2] == 'dan':
                    temp.append(' ')
            except:
                pass
            temp.append(string[i])
        hardFilter = ''.join(temp)
        tahun_ajar = softFilter[3:12]

        if softFilter[:3] == 'ATA':
            tahun = tahun_ajar[-4:]
        else:
            tahun = tahun_ajar[:4]
            
        return hardFilter

    def getCourseList(self):
        self.openPageOnAuth(self.site['DASHBOARD'])

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'coursename'))
            WebDriverWait(self.driver, 3).until(element_present)
        except TimeoutException:
            pass

        sauce = bs(self.driver.page_source, 'html.parser')
        cList = sauce.findAll('li', {'class': 'course-listitem'})
        data = []

        for course in cList:
            # Get anchor tag from html
            cItem = course.find('a', {'class': 'coursename'})

            # Course progress percentage
            try:
                progress = course.find('strong').text
            except:
                progress = None

            # Course name
            name = self.filterCourseName(cItem.text)

            # Course link
            id = cItem.attrs.get('href')[-4:]

            # Pack valuable info into a dictionary
            data.append({
                'courseId': id,
                'courseName': name,
                'courseProgress': progress
            })

        return data

    def getCourseTopics(self, course):
        self.openPageOnAuth(self.site['COURSE']+'?id='+course['courseId'])

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'topics'))
            WebDriverWait(self.driver, 3).until(element_present)
        except TimeoutException:
            pass

        sauce = bs(self.driver.page_source, 'html.parser')
        courseTopics = []
        topics = sauce.findAll('li', {'class': 'section main clearfix'})

        for topic in topics:
            topicTitle = topic.attrs.get('aria-label')
            topicActivites = []
            activities = topic.findChildren('li', {'class': 'activity'})

            for activity in activities:
                actLink = activity.find('a').attrs.get('href')
                actTitle = activity.find('span', {'class': 'instancename'}).text
                actType = activity.find('span', {'class': 'accesshide'}).text.replace(' ', '') if activity.find('span', {'class': 'accesshide'}) else None
                actComplete = 'Completed' in activity.find('img', {'class': 'icon'}).attrs.get('alt') if activity.find('img', {'class': 'icon'}) else None
                
                if actType == None:
                    if 'quiz' in actLink:
                        actType = 'Quiz'
                    elif 'forum' in actLink:
                        actType = 'Forum'
                    elif 'resource' in actLink:
                        actType = 'File'
                    elif 'assign' in actLink:
                        actType = 'Assignment'
                    elif 'chat' in actLink:
                        actType = 'Chat'

                if actType == 'Assignment':
                    if 'materi' in actTitle.lower():
                        actType = 'File'

                topicActivites.append({
                    'actTitle': actTitle,
                    'actLink': actLink,
                    'actType': actType,
                    'actComplete': actComplete,
                })

            courseTopics.append({
                'topicTitle': topicTitle,
                'topicActivities': topicActivites
            })
        
        course['courseTopics'] = courseTopics

    def getActDeadline(self, act):
        self.openPageOnAuth(act['actLink'])
        sauce = bs(self.driver.page_source, 'html.parser')
        # Get act start and deadline date
        data = None
        start = None
        deadline = None
        if act['actType'] == 'Assignment':
            data = sauce.find('table', {'class': 'generaltable'}).findChildren('td', {'class': 'cell c1 lastcol'})[:3]
            try:
                data1 = sauce.find('div', {'class': 'box py-3 generalbox boxaligncenter submissionsalloweddates'}).find('strong')
                start = datetime.datetime.strptime(data1.text, '%A, %d %B %Y, %I:%M %p')
            except:
                pass
            for datum in data:
                try:
                    deadline = datetime.datetime.strptime(datum.text, '%A, %d %B %Y, %I:%M %p')
                except:
                    pass
        if act['actType'] == 'Quiz':
            data = sauce.find('div', {'class': 'box py-3 quizinfo'}).findChildren('p')
            for datum in data:
                if 'opened' in datum.text:
                    strip = datum.text.replace('This quiz opened at ', '').replace('.', '')
                    start = datetime.datetime.strptime(strip, '%A, %d %B %Y, %I:%M %p')
                if 'until' in datum.text:
                    strip = datum.text.replace('The quiz will not be available until ', '').replace('.', '')
                    start = datetime.datetime.strptime(strip, '%A, %d %B %Y, %I:%M %p')
                if 'close' in datum.text:
                    strip = datum.text.replace('This quiz will close on ', '').replace('This quiz closed on ', '').replace('.', '')
                    deadline = datetime.datetime.strptime(strip, '%A, %d %B %Y, %I:%M %p')
        if act['actType'] == 'Forum':
            data = sauce.findAll('div', {'class': 'alert'})
            for datum in data:
                # TODO Get start date
                if 'due' in datum.text:
                    text = datum.text.strip().replace('The due date for posting to this forum', '').replace('is', '').replace('was', '').replace('.', '').replace(' ', '')
                    deadline = datetime.datetime.strptime(text, '%A,%d%B%Y,%I:%M%p')

        # Update act dict
        act['actStart'] = start
        act['actDeadline'] = deadline

        return act

    def getUpcomingTasks(self):
        courses = self.getCourseData()
        res = []
        for course in courses:
            topic_list = course['courseTopics']
            course_progress = course['courseProgress']
            if course_progress:
                for topic in topic_list[1:]:
                    activity_list = topic['topicActivities']
                    if activity_list:
                        for activity in activity_list:
                            if not activity['actComplete']:
                                if not(activity['actType'] == 'File' or activity['actType'] == 'Chat' or activity['actType'] == 'URL'):
                                    activity['actTitle'] = activity['actTitle'] + ' ({})'.format(course['courseName'])
                                    print(activity)
                                    res.append(self.getActDeadline(activity))

        try:
            res = sorted(res, key=lambda k: k['actDeadline'])
        except:
            temp = []
            for i, task in enumerate(res):
                if not task['actDeadline']:
                    temp.append(task)
            res = sorted([a for a in res if a not in temp], key=lambda k: k['actDeadline'])
            res = [a for a in res if a['actDeadline'] >= datetime.datetime.today()] + temp
            
        return res

    def getCourseData(self):
        courses = self.getCourseList()
        for course in courses:
            self.getCourseTopics(course)

        return courses