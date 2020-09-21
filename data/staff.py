from utils.proxy import OpenWeb

from difflib import SequenceMatcher
import re

website = {
    'MAIN': 'http://staffsite.gunadarma.ac.id/index2.php'
}

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getStaffList():
    with OpenWeb(website) as proxy:
        result = []
        staffSauce = proxy.getSauce(expectedTagName='table')
        staffList = staffSauce.find('table', {'width': '80%'}).findAll('td', attrs=None)

        for staffItem in staffList:
            staffName = staffItem.text.title().replace('[Email]', '').replace('[Homesite]', '')
            staffHomesite = staffItem.find('a', string='homesite')
            staffEmail = staffItem.find('a', string='email')
            if len(staffName.replace(' ','')) > 1 and staffName != 'Top' :
                result.append({
                    'staffName': re.sub(r'(\W+$)', '', staffName),
                    'staffHomesite': staffHomesite['href'] if staffHomesite else staffHomesite,
                    'staffEmail': staffEmail['href'].replace('mailto:', '') if staffEmail else staffEmail
                })
                
        return result

def getStaffInfo(staffName):
    possibleStaff = []
    staffList = getStaffList()

    for staff in staffList:
        similarity = similar(staff['staffName'], staffName)
        if (similarity == 1):
            return staff
        elif (similarity >= 0.8):
            print(staff)
            possibleStaff.append(staff)
    
    return possibleStaff