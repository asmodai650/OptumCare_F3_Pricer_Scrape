import argparse
import datetime
import time
import pymssql
import pyautogui as pa
import uuid
import getpass
import os
import __main__

from datetime import datetime
from sikuliWrapper import *


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


############## python3 scrape.py --q 'OptumCare Facets F3 Pricer Low Priority' --sqlu 'MS ID' --sqlp 'MS PASS' ##############
############## python3 scrape.py --q 'OptumCare Facets F3 Pricer' --sqlu 'MS ID' --sqlp 'MS PASS' ##############


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

#region COORDINATES

def hcpTabHeader():
    x = str(430)
    y = str(117)
    hcpTab = x, y
    return hcpTab

#endregion COORDINATES

#region FUNCTIONS

def yesNo(active = False):
    print("Starting yesNo data check")
    try:
        if active == True:
            pa.moveTo(x = 750, y = 10)
            yesno = input("Is this right?").lower()
            print(yesno)
            if yesno == "no":
                #quit(1)
                raise Exception("Quitting scrape from yesNo!")
            else:
                time.sleep(1)
                pa.moveTo(x = 750, y = 10)
                pa.click(x = 750, y = 10)
    except:
        raise Exception("Error in yesNo!")


def maximizeScreen():
    print("Starting maximizeScreen.")
    try:
        facetTopBar = pa.locateOnScreen(os.path.join(imgLocation, 'FacetsTopBar.png'), confidence=.7)
        if facetTopBar is not None: 
            print("Found FacetsTopBar.")
            pa.rightClick(facetTopBar)
            time.sleep(0.5)
            pa.press('up')
            time.sleep(0.5)
            pa.press('up')
            time.sleep(0.5)
            pa.press('enter')
            time.sleep(1)

        pa.moveTo(x = 120, y = 900)
        pa.click()
    except:
        raise Exception("Error in maximizeScreen!")


def checkScreenSize():
    print("Starting checkScreenSize")
    try:      
        # Check to see if Facets is still maximized
        windowMax = pa.locateOnScreen(os.path.join(imgLocation, 'windowMax.png'), confidence=.9)
        facetsApplications = pa.locateOnScreen(os.path.join(imgLocation, 'alreadyInFacetsCropped.png'), confidence=.7)

        if windowMax is not None and facetsApplications is not None:
            return
        else:
            #moveCitrixPopup()
            # Determine Facets Workspace. Can be different depending on state of window.
            fw1 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace1.png'), confidence=.7)
            fw2 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace2.png'), confidence=.7)
            fw3 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace3.png'), confidence=.7)

            if fw1 is not None:
                facetTab = fw1
            elif fw2 is not None:
                facetTab = fw2               
            elif fw3 is not None:
                facetTab = fw3
            else:
                raise Exception("Error in checkScreenSize!")

            pa.rightClick(facetTab)
            time.sleep(0.5)

            # Determine Workspace options based on state of window
            dropdownUmin = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspaceUnminDropdown.png'), confidence=.9)
            dropdownMax = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspaceMaxDropdown.png'), confidence=.9)

            # Found Option to maximize screen
            if dropdownMax is not None:
                pa.press('down')
                time.sleep(0.25)
                pa.press('x') # Maximize
                time.sleep(.5)
                pa.moveTo(x = 350, y = 200)
            # Found Option to Unminimize screen. This will restore it to its previous state, which might not be fully maximized
            elif dropdownUmin is not None:
                pa.press('down')
                time.sleep(0.25)
                pa.press('n') # Unminimized
                time.sleep(.5)
                pa.moveTo(x = 350, y = 200)

                # Check again for Workspace options based on new state of window
                pa.rightClick(facetTab)
                time.sleep(0.5)

                dropdownMax2 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspaceMaxDropdown.png'), confidence=.9)
                
                # If this is found, window is back on screen but not maximized
                if dropdownMax2 is not None:
                    pa.press('down')
                    time.sleep(0.25)
                    pa.press('x') # Maximize
                    time.sleep(.5)
                    pa.moveTo(x = 350, y = 200)
                
                # If this is found Facets window should be back to maximized
                facetsApplications2 = pa.locateOnScreen(os.path.join(imgLocation, 'alreadyInFacetsCropped.png'), confidence=.9)
                if facetsApplications2:
                    print("Found facetsApplications")
                else:
                    raise Exception("Error in checkScreenSize!")
        pa.moveTo(x = 120, y = 900)
        pa.click()
        return
    except:
        raise Exception("Error in checkScreenSize!")


def findSophia():
    print("Looking for Sophia")
    try:
        hcpTab = hcpTabHeader()
        goldenGirl1 = pa.locateOnScreen(os.path.join(imgLocation, 'findSophia.png'), confidence=.9, region=(1600, 900, 1900, 1100))
        goldenGirl2 = pa.locateOnScreen(os.path.join(imgLocation, 'findSophiaBlue.png'), confidence=.9, region=(1600, 900, 1900, 1100))

        if goldenGirl1 is not None or goldenGirl2 is not None:
            pa.click(hcpTab)
        else:
            raise Exception("Error in findSophia! Close and Restart Facets")
    except:
        raise Exception("Error in findSophia!")


def setIndicative():
    print("Setting screen to Indicative")
    try:
        #moveCitrixPopup()

        hcpTab = hcpTabHeader()
        pa.moveTo(hcpTab)
        pa.click(hcpTab)
        time.sleep(0.25)

        noWarnings = pa.locateOnScreen(os.path.join(imgLocation, 'moreProcessed.png'), confidence=.7, region=(750, 550, 900, 600))
        if noWarnings is None:
            time.sleep(.5)
            indicativeG = pa.locateCenterOnScreen(os.path.join(imgLocation, 'indicativeGrey.png'), confidence=.9, region=(30, 100, 200, 200))
            indicativeW = pa.locateCenterOnScreen(os.path.join(imgLocation, 'indicativeWhite.png'), confidence=.9, region=(30, 100, 200, 200))
        
            if indicativeG is not None:
                pa.doubleClick(indicativeG)
            elif indicativeW is not None:
                pa.doubleClick(indicativeW)
            else:
                raise Exception("Error in setIndicative! Cannot get back to Indicative screen")

        time.sleep(.25)
    except:
        raise Exception("Error in setIndicative!")


def checkFacetsWarning(screenType):
    print(f"Starting checkFacetsWarning. ScreenType is: {screenType}")
    try:        
        #moveCitrixPopup()

        valid = True
        facetErrorType = ''
        if screenType == 'Indicative':
            noWarnings = pa.locateOnScreen(os.path.join(imgLocation, 'moreProcessed.png'), confidence=.7, region=(750, 550, 900, 600))
        elif screenType == 'LineItems':
            noWarnings = pa.locateOnScreen(os.path.join(imgLocation, 'networkIndicator.png'), confidence=.7)
        else:
            raise Exception("Cannot determine ScreenType for closeWarnings!")

        warningStartTime = time.time()

        if noWarnings is None and time.time()-warningStartTime <= 30:
            try:
                if time.time()-warningStartTime > 30:
                    raise Exception("Inside Loop. Scrape took too long in checkFacetsWarning!")

                facetErrorX = pa.locateOnScreen(os.path.join(imgLocation, 'facetErrorX.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if facetErrorX is not None:
                    facetPopUp = facetErrorX
                    validclaim = closeFacetWarningBox(facetPopUp)
                    return validclaim

                facetTriangle1 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsTriangle.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if facetTriangle1 is not None:
                    facetPopUp = facetTriangle1
                    validclaim = closeFacetWarningBox(facetPopUp)
                    return validclaim

                facetTriangle2 = pa.locateOnScreen(os.path.join(imgLocation, 'FacetErrorTriangle2.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if facetTriangle2 is not None:
                    facetPopUp = facetTriangle2
                    validclaim = closeFacetWarningBox(facetPopUp)
                    return validclaim

                facetsTriangle = pa.locateOnScreen(os.path.join(imgLocation, 'facetsTriangle.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if facetsTriangle is not None:
                    facetPopUp = facetsTriangle
                    validclaim = closeFacetWarningBox(facetPopUp)
                    return validclaim

                openFailed = pa.locateOnScreen(os.path.join(imgLocation, 'openFailed.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if openFailed is not None:
                    facetPopUp = openFailed
                    validclaim = closeFacetWarningBox(facetPopUp)
                    return validclaim

                fileReservation = pa.locateOnScreen(os.path.join(imgLocation, 'fileReservation.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if fileReservation is not None:
                    facetPopUp = fileReservation
                    validclaim = closeFacetWarningBox(facetPopUp)
                    return validclaim
            
                time.sleep(1)

                warningsCleared = None
                if screenType == 'Indicative':
                    warningsCleared = pa.locateOnScreen(os.path.join(imgLocation, 'moreProcessed.png'), confidence=.7, region=(750, 550, 900, 600))
                    if warningsCleared is not None:
                        valid = False
                        validclaim = {'valid':valid, 'facetErrType':facetErrorType}
                        return validclaim
                    else:
                        closeWarnings(screenType, fromFacets = False)
                        valid = valid
                        validclaim = {'valid':valid, 'facetErrType':facetErrorType}
                        return validclaim
                elif screenType == 'LineItems':
                    warningsCleared = pa.locateOnScreen(os.path.join(imgLocation, 'networkIndicator.png'), confidence=.7)
                    if warningsCleared is not None:
                        valid = valid
                        validclaim = {'valid':valid, 'facetErrType':facetErrorType}
                        return validclaim
                    else:
                        closeWarnings(screenType, fromFacets = True)
                        valid = valid
                        validclaim = {'valid':valid, 'facetErrType':facetErrorType}
                        return validclaim
            except:
                raise Exception("Error in While Loop for checkFacetsWarning!")        
        validclaim = {'valid':valid, 'facetErrType':facetErrorType}
        return validclaim
    except:
        raise Exception("Error in checkFacetsWarning!")


def closeFacetWarningBox(facetPopUp):
    print("Starting closeFacetWarningBox.")
    try:
        valid = True
        facetErrorType = ''

        time.sleep(1)

        popupText = None
        popupText = Region(700, 400, x2 = 1250,y2 = 700).text()
        readonly = 'Read-Only?'
        cantPrice = 'cannot be recalled'
        openFailed = 'Open Failed'

        if popupText.find(readonly) != -1:
            valid = False
            facetErrorType = 'read only'
        elif popupText.find(cantPrice) != -1:
            valid = False
            facetErrorType = 'cannot be recalled'
        elif popupText.find(openFailed) != -1:
            valid = False
            facetErrorType = 'open failed'
        else:
            # If this warning or previous warning was severe, set to false, if not set to true
            valid = valid
            facetErrorType = 'unknown error'

        pa.click(facetPopUp)
        time.sleep(.25)
        pa.press('enter')
        time.sleep(.25)

        pa.moveTo(x = 430, y = 117)
        time.sleep(.5)

        closeFacetResult = {'valid':valid, 'facetErrorType':facetErrorType}
        return closeFacetResult
    except:
        raise Exception("Error in closeFacetWarningBox!")


def closeWarnings(screenType, fromFacets):
    print("Starting closeWarnings.")
    try:
        time.sleep(1)
        
        warnErrorType = ''

        if screenType == 'Indicative':
            noWarnings = pa.locateOnScreen(os.path.join(imgLocation, 'moreProcessed.png'), confidence=.7, region=(750, 550, 900, 600))
        elif screenType == 'LineItems':
            noWarnings = pa.locateOnScreen(os.path.join(imgLocation, 'networkIndicator.png'), confidence=.7)
        else:
            raise Exception("Cannot determine ScreenType for closeWarnings!")

        warningStartTime = time.time()

        while noWarnings is None and time.time()-warningStartTime <= 30:
            try:
                if time.time()-warningStartTime > 30:
                    raise Exception("Inside Loop. Scrape took too long in closeWarnings!")

                warn1 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'warningMessages.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if warn1 is not None:    
                    warningPopUp = warn1
                    closeWarningBox(warningPopUp)
                    if warnErrorType != '':
                        warnErrorType = warnErrorType
                warn2 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'warningMessages2.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if warn2 is not None:    
                    warningPopUp = warn2
                    closeWarningBox(warningPopUp)
                    if warnErrorType != '':
                        warnErrorType = warnErrorType

                warnAndError1 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'warningAndErrorMessage1.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if warnAndError1 is not None:
                    warningPopUp = (warnAndError1.x, warnAndError1.y + 15)
                    closeWarningBox(warningPopUp)
                    warnErrorType = 'claim error popup message'
                warnAndError2 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'warningAndErrorMessage2.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if warnAndError2 is not None:    
                    warningPopUp = (warnAndError2.x, warnAndError2.y + 15)
                    closeWarningBox(warningPopUp)
                    warnErrorType = 'claim error popup message'

                error1 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'errorMessages1.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if error1 is not None:    
                    warningPopUp = error1
                    closeWarningBox(warningPopUp)
                    warnErrorType = 'claim error popup message'
                error2 = pa.locateCenterOnScreen(os.path.join(imgLocation, 'errorMessages2.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if error2 is not None:    
                    warningPopUp = error2
                    closeWarningBox(warningPopUp)
                    warnErrorType = 'claim error popup message'

                if fromFacets == False:
                    facetErrorX = pa.locateOnScreen(os.path.join(imgLocation, 'facetErrorX.png'), confidence=.9, region=(700, 400, 1250 ,700))
                    if facetErrorX is not None:
                        facetPopUp = facetErrorX
                        closeFacetWarningBox(facetPopUp)
                        warnErrorType = 'facet error x while pricing'
                    facetTriangle1 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsTriangle.png'), confidence=.9, region=(700, 400, 1250 ,700))
                    if facetTriangle1 is not None:
                        facetPopUp = facetTriangle1
                        closeFacetWarningBox(facetPopUp)
                        warnErrorType = 'facet error triangle while pricing'
                    facetTriangle2 = pa.locateOnScreen(os.path.join(imgLocation, 'FacetErrorTriangle2.png'), confidence=.9, region=(700, 400, 1250 ,700))
                    if facetTriangle2 is not None:
                        facetPopUp = facetTriangle2
                        closeFacetWarningBox(facetPopUp)
                        warnErrorType = 'facet error triangle while pricing'
                    facetsTriangle = pa.locateOnScreen(os.path.join(imgLocation, 'facetsTriangle.png'), confidence=.9, region=(700, 400, 1250 ,700))
                    if facetsTriangle is not None:
                        facetPopUp = facetsTriangle
                        closeFacetWarningBox(facetPopUp)
                        warnErrorType = 'facet error triangle while pricing'

                hipaa1 = pa.locateOnScreen(os.path.join(imgLocation, 'hipaaPrivacyPopup.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if hipaa1 is not None:
                    pa.moveTo(hipaa1)
                    pa.press('enter')
                    time.sleep(.25)
                    if warnErrorType != '':
                        warnErrorType = warnErrorType

                hipaa2 = pa.locateOnScreen(os.path.join(imgLocation, 'HIPAA.png'), confidence=.9, region=(700, 400, 1250 ,700))
                if hipaa2 is not None:
                    pa.moveTo(hipaa2)
                    pa.press('enter')
                    time.sleep(.25)
                    if warnErrorType != '':
                        warnErrorType = warnErrorType

                checkAgain = None
                if screenType == 'Indicative':
                    checkAgain = pa.locateOnScreen(os.path.join(imgLocation, 'moreProcessed.png'), confidence=.7, region=(750, 550, 900, 600))
                    if checkAgain is not None:
                        #print("No more warning pop-ups remain.")
                        break
                elif screenType == 'LineItems':
                    checkAgain = pa.locateOnScreen(os.path.join(imgLocation, 'networkIndicator.png'), confidence=.7)
                    if checkAgain is not None:
                        noWarnings = ''
                        closeWarnResult = {'result':warnErrorType}
                        #print(f"No more warning pop-ups remain. closeWarnResult: {warnErrorType}")
                        return closeWarnResult 
            except:
                raise Exception("Error in While Loop for closeWarnings!")

        closeWarnResult = {'result':warnErrorType}
        #print(f"Leaving closeWarnings. closeWarnResult: {warnErrorType}")
        return closeWarnResult 
    except:
        raise Exception("Error in closeWarnings!")


def closeWarningBox(warningPopUp):
    print("Starting closeWarningBox.")    
    try:
        pa.click(warningPopUp)
        time.sleep(.5)
        pa.rightClick(warningPopUp)
        time.sleep(.25)
        pa.press('up')
        time.sleep(.25)
        pa.press('enter')
        time.sleep(.25)

        pa.moveTo(x = 975, y = 100)
        time.sleep(.5)

    except:
        raise Exception("Error in closeWarningBox!")


def alwaysVisible():
    # Set Workspace to 'Always on Visible Workspace'
    # Prevents Facets screen from going into another workspace when screen is not responsive while pricing claim
    print("Starting alwaysVisible.")
    try:
        fw1 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace1.png'), confidence=.5)
        if fw1 is not None:
            pa.moveTo(fw1)
            pa.rightClick(fw1)
        else:
            fw2 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace2.png'), confidence=.5)
            if fw2 is not None:
                pa.moveTo(fw2)
                pa.rightClick(fw2)
            else:
                fw3 = pa.locateOnScreen(os.path.join(imgLocation, 'facetsWorkspace3.png'), confidence=.5)
                if fw3 is not None:
                    pa.moveTo(fw3)
                    pa.rightClick(fw3)
                else:
                    raise Exception("Error in alwaysVisible!")

        time.sleep(0.5)
        pa.press('down')
        time.sleep(0.25)
        pa.press('a')
        time.sleep(.5)
        pa.moveTo(x = 350, y = 200)
        time.sleep(.5)

    except:
        raise Exception("Error in alwaysVisible!")


def moveCitrixPopup():    
## Look for Citrix pop up and if found move it to new workspace
    print("Starting moveCitrixPopup")    
    try:
        citrixPopup = pa.locateCenterOnScreen(os.path.join(imgLocation, 'citrixWorkspacePopup.png'), confidence=.9)
        citrixGrey = pa.locateCenterOnScreen(os.path.join(imgLocation, 'citrixWorkspaceGrey.png'), confidence=.9)
        citrixWhite = pa.locateCenterOnScreen(os.path.join(imgLocation, 'citrixWorkspaceWhite.png'), confidence=.9)

        if citrixPopup is not None:
            pa.rightClick(citrixPopup)
        elif citrixGrey is not None:
            pa.rightClick(citrixGrey)
        elif citrixWhite is not None:
            pa.rightClick(citrixWhite)
        else:
            return

        time.sleep(0.5)
        pa.press('up')
        time.sleep(0.5)
        pa.press('up')
        time.sleep(0.5)
        pa.press('right')
        time.sleep(0.5)
        pa.press('4') # workspace 4
        time.sleep(1)

        return

    except Exception as e:
        print("Error in moveCitrixPopup().")
        raise e


def findLineItems():
    print("Starting findLineItems.")
    try:
        time.sleep(0.5)

        lineItems1 = pa.locateOnScreen(os.path.join(imgLocation, 'lineItems.png'), confidence=.9)
        lineItemsBlue = pa.locateOnScreen(os.path.join(imgLocation, 'lineItemsBlue.png'), confidence=.9)
        lineItemsGray = pa.locateOnScreen(os.path.join(imgLocation, 'lineItemsGray.png'), confidence=.9)

        if lineItems1 is not None:
            pa.moveTo(lineItems1)
            pa.doubleClick(lineItems1)
            foundLineItems = True
        elif lineItemsBlue is not None:
            pa.moveTo(lineItemsBlue)
            pa.doubleClick(lineItemsBlue)
            foundLineItems = True
        elif lineItemsGray is not None:
            pa.moveTo(lineItemsGray)
            pa.doubleClick(lineItemsGray)
            foundLineItems = True
        else:
            foundLineItems = False
        
        time.sleep(.5)
        return foundLineItems

    except:
        raise Exception("Error in findLineItems!")


#endregion FUNCTIONS

#region SQL

def resultsToTable(claim_no, Charges, Allowed, Benefit, FacetError, FacetErrorType):
    print("Starting resultsToTable.")
    try:
        Date_Insert = datetime.now()
        connection = pymssql.connect(host = 'WP000075696.ms.ds.uhc.com', database = 'RacerResearch', user = msid, password = password)
        cursor = connection.cursor()
        query = "INSERT INTO racerresearch.[DBDataAnalytics-DM].OptumCare_Facets_F3_Pricer_Results (CLAIM_NO, Charges, Allowed, Benefit, Date_Insert, MSID, Facet_Error, Facet_Error_Type) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (claim_no, Charges, Allowed, Benefit, Date_Insert, UserMSID, FacetError, FacetErrorType))

        connection.commit()
        connection.close()

        time.sleep(0.5)

    except:
        raise Exception("Error in resultsToTable!")


def nullAmtCheck():
    ###### QUERIES RESULTS TABLE TO LOOK FOR ALLOWED AMOUNTS ######
    ###### IF MORE THAN 15 IN 5 MINUTES FROM ALL USERS THE SCRAPE STOPS ######
    print("Starting null amount Check.")
    try:
        connection = pymssql.connect(host = 'WP000075696.ms.ds.uhc.com', database = 'RacerResearch', user = msid, password = password)    
        cursor = connection.cursor()
        sqlUser = UserMSID

        query = """ SELECT COUNT(claim_no) AS claims
                    FROM racerresearch.[DBDataAnalytics-DM].OptumCare_Facets_F3_Pricer_Results WITH (NOLOCK)
                    WHERE (allowed IS NULL OR allowed = '0.00')
                    AND facet_error <> 1
                    AND (DATEDIFF(second, Date_Insert, GETDATE()) / 3600.0) < 0.085
                    AND MSID = %s """

        cursor.execute(query, (sqlUser))
        results = cursor.fetchall()
        connection.commit
        connection.close()

        sqlCount = (results[-1][-1])
        sqlCount = int(sqlCount)

        if sqlCount is None or sqlCount == 0:
            sqlCount == 0

        #if sqlCount > 15:
        #    raise Exception(f"Scrape is not finding allowed amounts!")

        time.sleep(0.5)
        return sqlCount
    except:
        raise Exception("Error in nullAmtCheck!")


def claimFindCheck():
    ###### QUERIES RESULTS TABLE TO LOOK FOR NULL ALLOWED AMOUNTS WITH SPECIFIC ERROR TYPE######
    ###### IF MORE THAN 10 IN 15 MINUTES FROM THE SAME USER THE SCRAPE STOPS FOR THAT USER ######
    print("Starting claimFindCheck.")
    try:
        connection = pymssql.connect(host = 'WP000075696.ms.ds.uhc.com', database = 'RacerResearch', user = msid, password = password)    
        cursor = connection.cursor()
        sqlUser = UserMSID

        query = """ SELECT COUNT(claim_no) AS claims
                    FROM racerresearch.[DBDataAnalytics-DM].OptumCare_Facets_F3_Pricer_Results WITH (NOLOCK)
                    WHERE allowed IS NULL
                    AND facet_error_type = 'try except failed cannot find claim'
                    AND (DATEDIFF(second, Date_Insert, GETDATE()) / 3600.0) < .25 
                    AND MSID = %s """

        cursor.execute(query, (sqlUser))
        results = cursor.fetchall()
        connection.commit
        connection.close()

        errCount = (results[-1][-1])
        errCount = int(errCount)

        if errCount is None or errCount == 0:
            errCount == 0

        time.sleep(0.5)
        return errCount

    except:
        raise Exception("Error in claimFindCheck!")

#endregion SQL
