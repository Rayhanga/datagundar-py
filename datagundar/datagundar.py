from datagundar.data.vclass import Vclass
from getpass import getpass
import platform
import os
import time

OS = platform.system()
def clearScreen():
    os.system('cls' if OS == 'Windows' else 'clear')

vc = Vclass()
while not vc.auth:
    vc.login(input('Username for vclass: '), getpass('Password for vclass: '))
    clearScreen()
print('Successfully logged in')
time.sleep(2)

print('Getting upcoming tasks')
upcoming_tasks = vc.getUpcomingTasks()
clearScreen()

# Display weekly
# Display remaining days

for task in upcoming_tasks:
    title = task['actTitle']
    link = task['actLink']
    start = task['actStart'].strftime('%d-%m-%Y %H:%M:%S') if task['actStart'] else '???'
    deadline = task['actDeadline'].strftime('%d-%m-%Y %H:%M:%S') if task['actDeadline'] else '???'
    print('{}\nLINK: {}\nMULAI: {}\nDEADLINE: {}\n'.format(title, link, start, deadline))

vc.close()