import argparse
import datetime
import time
import traceback
import pymssql
import pyautogui as pa
import uuid
import getpass
import os
import __main__

from support import *
from scrape import *
from datetime import datetime
from sikuliWrapper import *
from ScrapeQManager import scrapeQ


#region ARGUMENTS

parser = argparse.ArgumentParser()
parser.add_argument('--sqlu', dest='SQLUSER')
parser.add_argument('--sqlp', dest='SQLPASS')
parser.add_argument('--u0', dest='CitrixUser')
parser.add_argument('--p0', dest='CitrixPass')
parser.add_argument('--q', dest='scrapeq')
parser.add_argument('--msid', dest='userMS')
parser.add_argument('--uuid', dest='uuid')
args, unknown = parser.parse_known_args()

############## python3 scrapeTest.py --q 'OptumCare Facets F3 Pricer Low Priority' --sqlu 'MS ID' --sqlp 'MS PASS' ##############
############## python3 scrapeTest.py --q 'OptumCare Facets F3 Pricer' --sqlu 'MS ID' --sqlp 'MS PASS' ##############

if args.SQLUSER is None:
    scriptuuid = str(uuid.uuid4()) #just a random unique number to identify which scrape was running
    msid = input('Enter MS ID: ')
    UserMSID = msid 
    password = getpass.getpass("Enter MS password (cursor won't move while typing): ")
    msid = f'MS\\{msid}'
    username = msid
    scrapeQName = ['OptumCare Facets F3 Pricer','OptumCare Facets F3 Pricer Low Priority']
else:
    username = args.SQLUSER
    password = args.SQLPASS
    scriptuuid = args.uuid
    scrapeQName = args.scrapeq
    userMS = args.userMS
    UserMSID = args.userMS
    if 'ms\\' not in username.lower():
        msid = f'MS\\{username}'
    else:
        msid = username

#endregion ARGUMENTS

#region VARIABLES

mainfolder = os.path.dirname(os.path.abspath(os.path.join(os.getcwd(), __main__.__file__)))
imgLocation = os.path.join(mainfolder,'scrapeimages')

projectid = '1394'

#endregion VARIABLES


#region FUNCTIONS

print("Will start scrape in 1 second....")
time.sleep(1)
setupFacets()
time.sleep(.5)
findSophia() # checks to make sure Facets screen is in right condition to price claims
time.sleep(.5)
moveCitrixPopup()
time.sleep(.5)

#def findimage(claim_no):
#    print(f"Searching for {claim_no} .")
#    pa.moveTo(x = 430, y = 117)
#    time.sleep(.5)
#    pa.click(x = 430, y = 117) #Hospital Claims Processing tab
#    time.sleep(.5)
#    pa.hotkey('ctrl', 'o')
#    time.sleep(1)
#    loopStarttime = time.time()
#    found = False

#    while not exists('openClaimID_OC.png'):
#        print("Starting while loop in searchClm.")
#        if time.time()-loopStarttime > 180:
#            raise Exception(f"While Loop reached timeout! Could not find claim search window for claim {claim_no}!")
#        if exists('openClaimID_OC.png'):
#            print("Found openClaimID_OC image. Exiting loop.")
#            found = True
#            break
#        if not exists('openClaimID_OC.png'):
#            print("Cant find openClaim image. Trying to open claim search.")
#            pa.moveTo(x = 430, y = 117)
#            time.sleep(.5)
#            pa.click(x = 430, y = 117) #Hospital Claims Processing tab
#            time.sleep(.5)
#            pa.hotkey('ctrl', 'o')
#            time.sleep(1)

#    if not found:
#        wait('openClaimID_OC.png', 10)
#        if pa.locateOnScreen(os.path.join(imgLocation, 'openClaimID_OC.png'), confidence=.5) is not None:
#            found = True
#        else:
#            raise Exception(f"Could not find claim search window for claim {claim_no}!")

#    time.sleep(0.5)
#    type(claim_no)
#    time.sleep(0.5)
#    pa.press('enter')
#    Region(700, 400, x2 = 1250,y2 = 700).waitVanish('openClaimID_OC.png', 60)
#    time.sleep(1)
#    print(f"Checking for warning messages before pricing claim {claim_no}.")

#    t = pa.locateOnScreen(os.path.join(imgLocation, 'FacetErrorTriangle.png'))
#    print(t)
#    yesNo(True)

#endregion FUNCTIONS

#claim_no = '222802151R00'
#findimage(claim_no)


    





