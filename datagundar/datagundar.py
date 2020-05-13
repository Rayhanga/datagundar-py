from datagundar.data.vclass import Vclass
from datagundar.data.jadwal import Jadwal
from getpass import getpass
import platform
import os
import time

OS = platform.system()
def clearScreen():
    os.system('cls' if OS == 'Windows' else 'clear')

def VC():
    vc = Vclass()
    while not vc.auth:
        vc.login(input('Username for vclass: '), getpass('Password for vclass: '))
        clearScreen()
    print('Successfully logged in')
    time.sleep(2)

    print('Getting upcoming tasks')
    upcoming_tasks = vc.getUpcomingTasks()
    clearScreen()
 
    #============ TODO ============#
    #   A) Display weekly          #
    #   B) Display remaining days  #
    #============ TODO ============#

    for task in upcoming_tasks:
        title = task['actTitle']
        link = task['actLink']
        start = task['actStart'].strftime('%d-%m-%Y %H:%M:%S') if task['actStart'] else '???'
        deadline = task['actDeadline'].strftime('%d-%m-%Y %H:%M:%S') if task['actDeadline'] else '???'
        print('{}\nLINK: {}\nMULAI: {}\nDEADLINE: {}\n'.format(title, link, start, deadline))

    vc.close()

def JADWAL():
    jd = Jadwal()
    jadwal = jd.getJadwalKelas(input('Input kelas: '))
    clearScreen()
    if jadwal:
        for hari, jadkul in jadwal.items():
            print(hari)
            for jk in jadkul:
                w = jk['waktu']
                m = jk['matkul']
                d = jk['dosen']
                r = jk['ruang']

                print('|{}| {} @ {} ({})'.format(w, m, r, d))
            print()
    else:
        print('Selected kelas is either not found or not supported yet')
    jd.close()

def MENU():
    while True:
        clearScreen()
        print('Pick one of these tasks that you want to be done:')
        print('(A) Check Upcoming Tasks')
        print('(B) Check Jadwal Kuliah')
        opt = input('A or B ? ').strip()

        clearScreen()
        if opt.upper() == 'A':
            VC()
        elif opt.upper() == 'B':
            JADWAL()
        else:
            print('Unkown answer: {}'.format(opt))
        input('Press any key to continue...')
        clearScreen()

        agn = False
        while True:
            again = input('Run another task (y/n)? ').strip()
            if again.lower() == 'y' or again.lower() == '':
                agn = True
                break
            elif again.lower() == 'n':
                agn = False
                break
            else:
                print('Unkown answer: {}'.format(again))
        
        if not agn:
            break
