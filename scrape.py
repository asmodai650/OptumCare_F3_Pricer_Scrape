import argparse
import datetime
import time
import traceback
import pyautogui as pa
import uuid
import getpass
import os
import __main__

from support import *
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


############## python3 scrape.py --q 'OptumCare Facets F3 Pricer Low Priority' --sqlu 'MS ID' --sqlp 'MS PASS' --msid 'MS ID' ##############
############## python3 scrape.py --q 'OptumCare Facets F3 Pricer' --sqlu 'MS ID' --sqlp 'MS PASS' --msid 'MS ID' ##############


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
hcpTab = hcpTabHeader()
#pa.FAILSAFE = False
#endregion VARIABLES

#region FUNCTIONS

def setupFacets():
    print("Starting setupFacets")
    try:
        # Check to see if Facets is ready to go
        if pa.locateOnScreen(os.path.join(imgLocation, 'alreadyInFacetsCropped.png'), confidence=.7) is not None:
            pa.moveTo(hcpTab)
            pa.click(hcpTab)
            time.sleep(.5)

            noWarnings = pa.locateOnScreen(os.path.join(imgLocation, 'moreProcessed.png'), confidence=.7, region=(750, 550, 900, 600))
            if noWarnings is None:
                setIndicative()
            time.sleep(.5)

            alwaysVisible()

            return
        else:
            alwaysVisible()
            time.sleep(.5)
            
            maximizeScreen()
            time.sleep(.5)

            # Claims Processing > Hospital Claims Processing
            
            pa.press('c') # Capitation
            time.sleep(0.25)
            pa.press('c') # Claims Processing
            time.sleep(0.25)
            pa.press('right') # Claims Processing Submenu
            time.sleep(0.25)
            pa.press('h') # Hospital Claims Processing
            time.sleep(0.25)
            pa.press('enter')

        wait('openWork.png', 15) # Wait up to 15 seconds for the Hospital Claims Processing tab to load
        if pa.locateOnScreen(os.path.join(imgLocation, 'openWork.png'), confidence=.5) is None:
            raise Exception("Hospital Claims Processing tab failed to load!")

    except:
        raise Exception("Error in setupFacets!")


def startScrapeF3(claim_no):
    print("Starting startScrapeF3.")
    try:
        try:
            checkScreenSize()
            #setIndicative()

            searchClmSuccess = searchClm(claim_no)

            if searchClmSuccess['valid'] == False:
                Charges = None
                Allowed = None
                Benefit = None
                FacetError = '1'
                if searchClmSuccess['facetErrorType'] is None or searchClmSuccess['facetErrorType'] == '':
                    FacetErrorType = 'search claim failed cannot find claim'
                else:
                    FacetErrorType = searchClmSuccess['facetErrorType']               
                resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)
                setIndicative()
                return

        except:
            Charges = None
            Allowed = None
            Benefit = None
            FacetError = '1'
            FacetErrorType = 'try except failed cannot find claim'
            resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)
            setIndicative()
            return

        time.sleep(.25)
        pa.moveTo(hcpTab)
        pa.click(hcpTab)
        time.sleep(.25)

        facetPopUp = pa.locateOnScreen(os.path.join(imgLocation, 'FacetErrorTriangle.png'))
        if facetPopUp is not None:
            closeFacetResult = closeFacetWarningBox(facetPopUp)
            time.sleep(1)
            if closeFacetResult['valid'] == False:
                anotherfacetPopUp = pa.locateOnScreen(os.path.join(imgLocation, 'FacetErrorTriangle.png'))
                if anotherfacetPopUp is not None:
                    pa.click(anotherfacetPopUp)
                    pa.press('enter')
                    time.sleep(1)
                    if pa.locateOnScreen(os.path.join(imgLocation, 'FacetErrorTriangle.png')) is not None:
                        raise Exception("FacetErrorTriangle did not disappear.")
            Charges = None
            Allowed = None
            Benefit = None
            FacetError = '1'
            if closeFacetResult['facetErrorType'] is None or closeFacetResult['facetErrorType'] == '':
                FacetErrorType = 'facet error triangle after search'
            else:
                FacetErrorType = closeFacetResult['facetErrorType']
            resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)
            setIndicative()
            return

        ximage = pa.locateOnScreen(os.path.join(imgLocation, 'facetErrorX.png'))
        if ximage is not None:
            pa.click(ximage)
            pa.press('enter')
            if pa.locateOnScreen(os.path.join(imgLocation, 'facetErrorX.png')) is not None:
                raise Exception("facetErrorX did not disappear.")
            pa.press('enter')
            Charges = None
            Allowed = None
            Benefit = None
            FacetError = '1'
            FacetErrorType = 'facet error x image after search'
            resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)
            setIndicative()
            return

        if pa.locateOnScreen(os.path.join(imgLocation, 'chargeAllowedBenefitLabelsOC.png'), confidence=.7) is None:
            moveCitrixPopup()
            pa.moveTo(hcpTab)
            time.sleep(.25)
            pa.click(hcpTab)
            time.sleep(.25)
            
            foundLineItems = findLineItems()

            if foundLineItems == False:
                checkScreenSize()

                if checkScreenSize():
                    foundLineItemsTwo = findLineItems()
                    if foundLineItemsTwo == False:
                        raise Exception("Could not find Line Items image.")
            
            time.sleep(.25)
            pa.moveTo(hcpTab)
            time.sleep(.25)

            if pa.locateOnScreen(os.path.join(imgLocation, 'chargeAllowedBenefitLabelsOC.png'), confidence=.7) is None:
                raise Exception("Could not get to Line Items tab.")

        time.sleep(.25)
        pa.moveTo(hcpTab)
        time.sleep(.25)

        priceClaim(claim_no)
        time.sleep(.5)

        setIndicative()

        pa.moveTo(hcpTab)
        time.sleep(.25)
        pa.click(hcpTab)

        print(f"Finished startScrapeF3 for claim {claim_no} . Leaving startScrapeF3.")

    except:
        raise Exception("Error in startScrapeF3!")


def searchClm(claim_no):
    print("Starting searchClm.")
    try:    
        screenType = 'Indicative'
        fromFacets = False

        print(f"Searching for {claim_no} .")
        pa.moveTo(hcpTab)
        time.sleep(.25)
        pa.click(hcpTab) #Hospital Claims Processing tab
        time.sleep(.5)
        pa.hotkey('ctrl', 'o')
        time.sleep(.5)

        openClaimWindow1 = pa.locateOnScreen(os.path.join(imgLocation, 'openClaimID_OC2.png'), confidence=.7, region=(700, 400, 1250, 700))

        if openClaimWindow1 is None:
            pa.click(hcpTab) #Hospital Claims Processing tab
            time.sleep(.5)
            pa.hotkey('alt', 'f')
            time.sleep(.5)
            pa.press('o')
            time.sleep(.5)

            openClaimWindow2 = pa.locateOnScreen(os.path.join(imgLocation, 'openClaimID_OC2.png'), confidence=.7, region=(700, 400, 1250, 700))

            if openClaimWindow2 is None:
                facetTopBar = pa.locateOnScreen(os.path.join(imgLocation, 'FacetsTopBar2.png'), confidence=.7)

                if facetTopBar is None:
                    raise Exception(f"Could not find claim search window for claim {claim_no}!")
                else:
                    ## if code reaches this point keyboard commands are probably NOT working
                    ## will need to use mouse to 'click' and open the claim search window
                    pa.click(hcpTab) #Hospital Claims Processing tab
                    time.sleep(.25)
                    l,t,w,h = pa.locateOnScreen(os.path.join(imgLocation, 'FacetsTopBar2.png'), confidence=.7)
                    time.sleep(0.5)
                    pa.moveTo(facetTopBar)
                    facetTopBarOffset = (l + 15, t + 15)
                    time.sleep(0.5)
                    pa.moveTo(facetTopBarOffset)
                    print(f"facetTopBar is: {facetTopBar}.")
                    time.sleep(0.5)
                    pa.click(facetTopBarOffset)
                    time.sleep(0.5)

                    fileMenu = (l + 15, t + 50)
                    time.sleep(0.5)
                    pa.moveTo(fileMenu)
                    time.sleep(0.5)
                    print(f"fileMenu is: {fileMenu}.")
                    pa.click(fileMenu)
                    time.sleep(0.5)

                    openClaimWindow3 = pa.locateOnScreen(os.path.join(imgLocation, 'openClaimID_OC2.png'), confidence=.7, region=(700, 400, 1250, 700))

                    if openClaimWindow3 is None:
                        raise Exception(f"Could not find claim search window for claim {claim_no}!")
                    else:
                        print("Clicking openClaimWindow3")
                        pa.click(openClaimWindow3)
            else:
                print("Clicking openClaimWindow2")
                pa.click(openClaimWindow2)
        else:
            print("Clicking openClaimWindow1")
            pa.click(openClaimWindow1)

        
        time.sleep(0.5)
        type(claim_no)
        time.sleep(0.5)
        pa.press('enter')

        Region(700, 400, x2 = 1250,y2 = 700).waitVanish('openClaimID_OC.png', 60)

        validclaim = checkFacetsWarning(screenType)

        closeWarnings(screenType, fromFacets)

        if validclaim['valid'] == False:
            return validclaim

        clmButtons = pa.locateOnScreen(os.path.join(imgLocation, 'mainCLMButtonsOC.png'), confidence=.7)

        if clmButtons is not None:
            time.sleep(0.5)
            return validclaim
        else:
            validclaim['valid'] = False
            return validclaim

    except:
        raise Exception("Error in searchClm!")


def priceClaim(claim_no):
    print("Starting priceClaim.")
    try:
        checkScreenSize()

        screenType = 'LineItems'
        fromFacets = False

        warnErr = closeWarnings(screenType, fromFacets)

        if warnErr['result'] != '':
            Charges = None
            Allowed = None
            Benefit = None
            FacetError = '1'
            if warnErr['result'] is None or warnErr['result'] == '':
                FacetErrorType = 'unknown facet error before pricing'
            else:
                FacetErrorType = warnErr['result']
            resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)
            return

        time.sleep(.25)
        pa.moveTo(hcpTab)
        time.sleep(.25)
        pa.press('f3')
        time.sleep(.5)

        loopStartTime = time.time()

        while time.time()-loopStartTime <= 300: #900
            try:
                if time.time()-loopStartTime > 300: #900
                    raise Exception("Repricing took longer than 5 minutes!")

                if (exists('adjudicationInProcess.png')
                    or
                    exists('notResponding.png')):
                    time.sleep(2)

                if (not exists('notResponding.png')
                    and
                    not exists('adjudicationInProcess.png')):
                    time.sleep(5)
                    if exists('facetsBottomLeftBlank.png'):
                        break ####### THIS LEAVES WHILE LOOP WHEN PRICING IS COMPLETE #######
                    else:
                        #time.sleep(.5)

                        ##workspace1 = pa.center(pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace1.png'), confidence=.5))
                        ##workspace2 = pa.center(pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace2.png'), confidence=.5))
                        ##workspace3 = pa.center(pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace3.png'), confidence=.5))      
                        #workspace1 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'facetsWorkspace1.png'), confidence=.5)
                        #workspace2 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'facetsWorkspace2.png'), confidence=.5)
                        #workspace3 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'facetsWorkspace3.png'), confidence=.5)     
            
                        #if workspace1 is not None:
                        #    workspace = workspace1
                        #elif workspace2 is not None:
                        #    workspace = workspace2
                        #elif workspace3 is not None:
                        #    workspace = workspace3
                        #else:
                        #    raise Exception("Cannot determine workspace in While Loop for priceClaim. Cannot find Facets Screen!")

                        #pa.click(workspace)
                        #time.sleep(.5)
                        pa.moveTo(hcpTab)
                        time.sleep(.5)

            except:
                raise Exception("Error in While Loop for priceClaim!")

        print("Exited out of startScrape While Loop. Looking for warning messages after pricing.")
        warnErr = closeWarnings(screenType, fromFacets)

        if warnErr['result'] != '':
            Charges = None
            Allowed = None
            Benefit = None
            FacetError = '1'
            if warnErr['result'] is None or warnErr['result'] == '':
                FacetErrorType = 'unknown facet error after pricing'
            else:
                FacetErrorType = warnErr['result']
            resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)
            return

        time.sleep(.5)
        checkScreenSize()

        print("Looking for amountAllowed.")
        
        if pa.locateOnScreen(os.path.join(imgLocation, 'chargeAllowedBenefitLabelsOC.png'), confidence=.7) is not None:
            CDleft, CDtop, CDwidth, CDheight = pa.locateOnScreen(os.path.join(imgLocation, 'chargeAllowedBenefitLabelsOC.png'), confidence=.7)

            allowedX1 = (CDleft + 55)
            allowedY1 = (CDtop + 18)
            tempAllowed = Region(allowedX1, allowedY1, w = 140, h = 17)

            dateconfig = {"mode": "block", "character_whitelist": "1234567890$"}
            amountAllowed = tempAllowed.text(dateconfig).replace("$", "")
        else:
            raise Exception(f"Cannot find Allowed benefit for claim {claim_no}!")

        if len(amountAllowed) < 3:
            Charges = None
            Allowed = None
            Benefit = None
            FacetError = '1'
            FacetErrorType = 'new priced amount allowed less than 3 characters'
            resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)
        else:
            try:
                amountFloat = float(amountAllowed)
                amountDec = amountFloat * 0.01
                amountAllowed = "{:.2f}".format(amountDec)
                Charges = None
                Allowed = amountAllowed
                Benefit = None
                FacetError = '0'
                FacetErrorType = None
                resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)
            except:
                Charges = None
                Allowed = None
                Benefit = None
                FacetError = '1'
                FacetErrorType = 'could not determine new priced amount allowed'
                resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType)

    except:
        raise Exception("Error in priceClaim!")


#endregion FUNCTIONS

#region MAIN

if __name__ == "__main__":
    try:
        print("Will start scrape in 3 seconds....")
        time.sleep(1)
        print("2...")
        time.sleep(1)   
        print("1...")
        time.sleep(1)

        setupFacets()
        time.sleep(.5)
        findSophia() # checks to make sure Facets screen is in right condition to price claims
        time.sleep(.5)
        moveCitrixPopup()
        time.sleep(.5)

        scrapeQueue = [scrapeQName]
        for qName in scrapeQueue:
            queueInventory = scrapeQ(msid, password, 'WP000075696.ms.ds.uhc.com', projectid, qName, mainuuid=scriptuuid, userMSid=UserMSID)
            scrapeStartTime = datetime.now()
            errorStartTime = time.time()

            claimCount = 0
            while queueInventory.nextItem():
                queueStartTime = time.time()
                body = queueInventory.getItem()
                claim_no = body
                time.sleep(.5)

                startScrapeF3(claim_no)

                claimCount += 1

                currentScrapeTime = time.time()
                errTime = float(300) #300 is 5 minutes / 60 is one minute / etc.

                nullCount = nullAmtCheck()
                print(f"nullCount: {nullCount}")
                errCount = claimFindCheck()
                print(f"errCount: {errCount}")

                if (nullCount >= 15) and (currentScrapeTime - errorStartTime >= errTime):
                    raise Exception(f"Scrape is not finding allowed amounts! Close and Restart Facets.")

                if (errCount >= 10) and (currentScrapeTime - errorStartTime >= errTime):
                    raise Exception(f"Scrape is not finding claims. Close and Restart Facets.")

                #claimTime = time.time()-queueStartTime
                #print(f"Claim took {claimTime} to scrape. Scraped a total of {claimCount} claims")

        scrapeEndTime = (datetime.now() - scrapeStartTime)
        print(f"No more claims in the queue. Scrape ran for {scrapeEndTime} .")

    except:
        errorTime = datetime.now()
        print(f"Error time: {errorTime}")
        with open(f'/home/headless/errorLog.log', 'w') as f:
            f.write(traceback.format_exc())
        print(traceback.format_exc())
        exit(1)

#endregion MAIN
