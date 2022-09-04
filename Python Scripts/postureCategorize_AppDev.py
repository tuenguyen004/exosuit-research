""" --------------------------
POSTURE-CATEGORIZING ALGORITHM (modified for AppDev Testing)
------------------------------
     > Created in Mid-August 2020 by Tue Nguyen'23
     > Taken from MATLAB and transfered into Python
 
    
# ============================================================================
# ====================== REQUESTING FOR THESE VALUES =========================
# ============================================================================
     
# time = time passed since recording

# x1 = x of ChestTop
# y1 = y of ChestTop (as in height)
# z1 = z of ChestTop
# originTop = [0,starting y1,0] assuming starting upright @time=0

# x2 = x of ChestBot
# y2 = y of ChestBot 
# z2 = z of ChestBot
# originBot = [0,starting y2,0] assuming starting upright @time=0

# x3 = x of Tummy
# y3 = y of Tummy
# z3 = z of Tummy
# originTummy = [0,starting y3,0] assuming starting upright @time=0

# frontback1 = anterior/posterior of Chest
# leftright1 = lateral of Chest
# rotate1 = rotation of Chest

# frontback2 = anterior/posterior of Hip
# leftright2 = lateral of Hip
# rotate2 = rotation of Hip

"""
time = 10;

x1 = 1;
y1 = 0.8;
z1 = 1;
originTop = [0,0.795,0]

x2 = 0.001;
y2 = 0.7;
z2 = 0.001;
originBot = [0,0.695,0]

x3 = 0.001;
y3 = 5;
z3 = 0.001;
originTummy = [0,0.495,0]

frontback1 = 10
leftright1 = 0
rotate1 = 0

frontback2 = -10
leftright2 = 0
rotate2 = 0


# ===========================================================================
import math
import numpy as np


#return a String object
def find_Motion_NotUpright(frontBack, leftRight):
    xStatus = ""
    zStatus = ""
    direction = ""
    
    # determining if X and/or Z direction are negative 
    # NOTE: right(+) and left(-) for tilting angle 
    if (leftRight > 10):        
        xStatus = "X-";
    elif (leftRight < -10):
        xStatus = "X";

    if (frontBack > 0):
        zStatus = "Z"
    elif (frontBack < 0):
        zStatus = "Z-";

    absLR = abs(leftRight);
    absFB = abs(frontBack);
    # determine the strength of each direction & finalize in a string variable
    if (absFB > 12 and absLR < 12):
        direction = zStatus
    elif (absFB < 12 and absLR > 12):
        direction = xStatus
    elif (absFB > 12 and absLR > 12):
        if (absLR > absFB):
            direction = xStatus + " " + zStatus
        elif (absLR < absFB):
            direction = zStatus + " " + xStatus
        else:
            direction = xStatus + " = " + zStatus
            
    return direction

#return a String object
def find_Direction_Leaving_Upright(x,z):
# Return a string of which direction(s) the object is leaving upright
    
    diff = abs(x) - abs(z)
    motionCheck = 0.02      # Threshold of x & z position before considered the presence of that
                            #   axis in the object's motion
    diffXZ = 0.03           # Threshold of x & z position before considered the presence of that
                            #   axis RELATIVE TO EACH OTHER in the object's motion 
    output = ""
                            
    if (abs(x) > motionCheck) or (abs(z) > motionCheck):
        if (diff > 0) and (abs(diff) > diffXZ):
            output = "X"
            if (x < 0):
                output = output + "-"

        elif(diff < 0) and (abs(diff) > diffXZ):
            output = "Z"
            if (z < 0):
                output = output + "-"

        elif(diff > 0) and (abs(diff) <= diffXZ):
            output = "X Z"
            if(x < 0 and z < 0):
                output = "X- Z-"
            elif(x < 0 and z > 0):
                output = "X- Z"
            elif(x > 0 and z < 0):
                output = "X Z-"

        elif(diff < 0) and (abs(diff) <= diffXZ):
            output = "Z X"
            if(x < 0 and z < 0):
                output = "Z- X-"
            elif(x < 0 and z > 0):
                output = "Z X-"
            elif(x > 0 and z < 0):
                output = "Z- X"
    return output




# ============================================================================
# ====================== POSTURE() CLASS DECLARATION =========================
# ============================================================================
    
# Posture() Object Class for Real-time Classification of the Subject's Posture
class Posture:
    #Default Constructor when object first call
    def __init__(self):
        self.upright = np.array([True,True,True,True])
        self.straightFront = True
        self.straightSide = True
        self.slouch = False
        self.twist = [False,""]
        
        self.numNotUpright = 0
        self.numNotStraight = 0         
        self.numSlouch = 0             
        self.numTwist = 0                   
        
        self.notUprightTime = []
        self.notStraightTime_Front = []
        self.notStraightTime_Side = []
        self.slouchTime = []
        self.twistTime_Left = []
        self.twistTime_Right = []
        
        self.bodyDirectionLeaving = np.array(["","",""])
        self.notUprightDirection = ""
        
    # Adding Time Duration to Specific Category
    # 1 = notUpright
    # 2 = notStraight
    # 3 = slouching
    # 4 = twisting
    def addTime(self,timeDuration,idTest):
        if (idTest == 1):
            self.notUprightTime.append(timeDuration)
        elif (idTest == 2):
            if (not self.straightFront):
                self.notStraightTime_Front.append(timeDuration)
            elif (not self.straightSide):
                self.notStraightTime_Side.append(timeDuration)
        elif (idTest == 3):
            self.slouchTime.append(timeDuration)
        elif (idTest == 4):
            if (self.twist[1] == "left"):
                self.twistTime_Left.append(timeDuration)
            elif (self.twist[1] == "right"):
                self.twistTime_Right.append(timeDuration)
        else:
            print("ERROR: ID out of bound for " + str(timeDuration))
        return
    
    # python.print formatting
    def __str__(self):
        print("")
        print("-----------  Current User's Posture & Orientation  -----------")
        print("")
        print("          upright (ChestTop): " + str(self.upright[0]))
        print("          upright (ChestBot): " + str(self.upright[1]))
        print("             upright (Tummy): " + str(self.upright[2]))
        print("        upright (wholeTorso): " + str(self.upright[3]))
        print("       back straight (front): " + str(self.straightFront))
        print("        back straight (side): " + str(self.straightSide))
        print("     slouching (Chest & Hip): " + str(self.slouch))
        print("   twisting (Chest Rotation): " + str(self.twist))
        print("")
        print("   leaving Upright Direction: " + str(self.bodyDirectionLeaving))
        print("   last notUpright Direction: " + str(self.notUprightDirection))
        print("")
        print("----------------  Movement Tracking Counters  ----------------")
        print("")
        print("   # notUpright (wholeTorso): " + str(self.numNotUpright))
        print("   # notStraight (both view): " + str(self.numNotStraight))
        print("                 # slouching: " + str(self.numSlouch))
        print("                  # twisting: " + str(self.numTwist))
        print("")
        print("--------  Time Durations (sec) of Movement Identified  -------")
        print("")
        print("              notUprightTime: "  + str(self.notUprightTime))
        print("       notStraightTime_Front: "  + str(self.notStraightTime_Front))
        print("        notStraightTime_Side: "  + str(self.notStraightTime_Side))
        print("                  slouchTime: "  + str(self.slouchTime))
        print("              twistTime_Left: "  + str(self.twistTime_Left))
        print("             twistTime_Right: "  + str(self.twistTime_Right))
        print("")
        
        return ""








# ----------------------------------------------------------------------------
# ----------------------- Variables for STATUS CHECK -------------------------
# ----------------------------------------------------------------------------
uprightDetect = np.array([True,True,True,True])     # eachBody (first three logical values) & wholeBody Status Check
straightDetect = np.array([True,True])              # straightback detected already or not, frontView & sideView 
straightCompleted = np.array([True,True])           # returned to Straight-Back or not, frontView & sideView 

slouchDetect = False                                # slouching status detect
twistRightDetect = False                            # rotating to right status detect 
twistLeftDetect = False                             # rotating to left status detect 

notStraightFrontCounted = False;                    
notStraightSideCounted = False;

axisMoved = np.array(["","",""]) 
notUprightDetect = ""
# ----------------------------------------------------------------------------
# --------------------- MARGIN OF ERRORS for Categorizing -------------------- 
# ----------------------------------------------------------------------------
uprightCheck = 0.065                    # Distance each parts must travel before considered not upright 
straightFrontCheck = 5                  # Back-aligning degree before FrontView not straight
straightSideCheck = 10                  # Back-aligning degree before SideView not straight

slouchChestCheck = 5                    # Front/Back angle (in degrees) of Chest before Slouching is detected
slouchHipCheck = -5                     # Front/Back angle (in degrees) of Hip before Slouching is detected
twistCheck = 15                         # Degree of Turn before recognized as body rotated

# Time recorded for a new NotStraight = must wait 0.1sec before a Straight signal can be received 
timeFront = 0                           
timeSide = 0                            
timeSlouch = 0                          
timeTwist = 0                           
timeNotUpright = 0                      









# Initiate 'subj' to hold posture-categorizing data 
subj = Posture()   
   







# ----------------------------------------------------------------------------
# ------------- Positional Calculation (distance & axis index) ---------------
# ----------------------------------------------------------------------------
currentTop = np.array([x1,y1,z1]) - originTop
maxTopAbs = max(abs(currentTop))
idxTop = np.argmax(abs(currentTop))
distTop = math.sqrt(currentTop[0]**2 + currentTop[2]**2)

currentBot = np.array([x2,y2,z2]) - originBot
maxBotAbs = max(abs(currentBot))
idxBot = np.argmax(abs(currentBot))
distBot = math.sqrt(currentBot[0]**2 + currentBot[2]**2)

currentTummy = np.array([x3,y3,z3]) - originTummy
maxTummyAbs = max(abs(currentTummy))
idxTummy = np.argmax(abs(currentTummy))
distTummy = math.sqrt(currentTummy[0]**2 + currentTummy[2]**2)

currentPosture = np.array([currentTop,currentBot,currentTummy])
distPosture = np.array([distTop,distBot,distTummy])

# ----------------------------------------------------------------------------
# ------ Angular Calculation (theta derivation of frontView & sideView) ------
# ----------------------------------------------------------------------------
radianToDegree = 180/np.pi

thetaFront1 = math.atan((x1 - x2) / (y1 - y2)) * radianToDegree
thetaFront2 = math.atan((x2 - x3) / (y2 - y3)) * radianToDegree
diffThetaFront = thetaFront1 - thetaFront2;

#print(diffThetaFront)
#print("\n")

thetaSide1 = math.atan((z1 - z2) / (y1 - y2)) * radianToDegree
thetaSide2 = math.atan((z2 - z3) / (y2 - y3)) * radianToDegree
diffThetaSide = thetaSide1 - thetaSide2;


aChestFB = frontback1;
aChestLR = leftright1;
aChestRot = rotate1;
aHipFB = frontback2;






                    # ========================
                    # ========================
                    # CATEGORIZING ALGORITHMS: 
                    # ========================
                    # ========================

# ----------------------------------------------------------------------------
# > BACK NOT STRAIGHT SIGNAL = identifying whether or not current positions of
#   ChestTop, ChestBottom, Tummy (three points representing the subject's 
#   upper torso) is aligned in a straight line
#   
# > Checking for the difference between angles of ChestTop & Tummy relative to 
#   ChestBottom from SideView and FrontView (ignore TopView angles because yield 
#   overlapping results with the two other views)
# ----------------------------------------------------------------------------
# ***** FRONT VIEW: BACK NOT STRAIGHT *****
if (abs(diffThetaFront) > straightFrontCheck) and (straightDetect[0]):
    timeFront = time
    straightDetect[0] = False
    straightCompleted[0] = False
    
# ***** SIDE VIEW: BACK NOT STRAIGHT *****
elif (abs(diffThetaSide) > straightSideCheck) and (straightDetect[1]):
    straightCompleted[1] = False     
    
    timeSide = time
    straightDetect[1] = False
# ***** FRONT VIEW: RETURNED TO STRAIGHT *****
elif (abs(diffThetaFront) <= straightFrontCheck) and (not straightDetect[0]):
    if (time-timeFront > 0.1):
        durationStraight = time - timeFront
        subj.addTime(durationStraight,2)
        subj.straightFront = True
        straightDetect[0] = True
        straightCompleted[0] = True
        notStraightFrontCounted = False
        
# ***** SIDE VIEW: RETURNED TO STRAIGHT *****
elif (abs(diffThetaSide) <= straightSideCheck) and (not straightDetect[1]):
    if (time-timeSide > 0.1):
        durationStraight = time - timeSide
        subj.addTime(durationStraight,2)
        subj.straightSide = True
        straightDetect[1] = True
        straightCompleted[1] = True
        notStraightSideCounted = False
        
# ----------------------------------------------------------------------------  
# > Only after one second, send out backNotStraight signal & save that status 
#   into Posture() class ==> otherwise don't do anything
# ----------------------------------------------------------------------------
# ***** frontView: back not straight for 1 second *****
if (not straightDetect[0]):
    if (time - timeFront > 0.5) and (not notStraightFrontCounted):
       subj.straightFront = False
       subj.numNotStraight = subj.numNotStraight + 1;
       notStraightFrontCounted = True;
       
# ***** sideView: back not straight for 1 second *****
if (not straightDetect[1]):
    if (time - timeSide > 0.5) and (not notStraightSideCounted):
       subj.straightSide = False
       subj.numNotStraight = subj.numNotStraight + 1;
       notStraightSideCounted = True;



# ----------------------------------------------------------------------------
# > SLOUCHING SIGNAL = identifying whether current posture is "slouching"
#
# > Checking for a positive Chest_Angle and a negative Hip_Angle         
# ----------------------------------------------------------------------------
# ***** Posture Slouching *****
if (aChestFB > slouchChestCheck) and (aHipFB < slouchHipCheck) and (not slouchDetect):
    subj.slouch = True;
    timeSlouch = time;
    slouchDetect = True;
# ***** Posture Not Slouching *****
elif (aChestFB <= slouchChestCheck) and (aHipFB >= slouchHipCheck) and (slouchDetect):
    durationSlouch = time - timeSlouch;
    subj.addTime(durationSlouch,3);
    subj.numSlouch = subj.numSlouch + 1;
    subj.slouch = False;
    slouchDetect = False;







# ----------------------------------------------------------------------------
# > TWISTING SIGNAL = identifying by checking Chest's rotation
#
# > Checking for a left/right rotational Chest_Angle
# ----------------------------------------------------------------------------
if (aChestRot > twistCheck) and (not twistLeftDetect):
    subj.twist = [True,"left"];
    timeTwist = time;
    twistLeftDetect = True;
elif (aChestRot < -twistCheck) and (not twistRightDetect):
    subj.twist = [True,"right"];
    timeTwist = time;
    twistRightDetect = True;
elif (aChestRot >= -twistCheck) and (aChestRot <= twistCheck) and (twistLeftDetect or twistRightDetect):
    durationTwist = time - timeTwist;
    subj.addTime(durationTwist,4)
    subj.numTwist = subj.numTwist + 1;
    subj.twist = [False,""];
    twistLeftDetect = False;
    twistRightDetect = False;





# ----------------------------------------------------------------------------
# NOTUPRIGHT DIRECTION SIGNAL = where body located/tilting or not 
#   once outside upright zone & tracking movement outside upright based
#   on body's angles not actual position (can track position by looking
#   at the body coordinates)
# Upright Detection is based on whether CHESTTOP is upright or not ONLY
# ----------------------------------------------------------------------------
direct = find_Motion_NotUpright(aChestFB,aChestLR);
if (not uprightDetect[0]) and (direct != notUprightDetect) and (direct != ""):
    notUprightDetect = direct;
    subj.notUprightDirection = direct;





# ----------------------------------------------------------------------------
# UPRIGHT SIGNAL = original upright posture where all three positions
#   (ChestTop, ChestBottom, Tummy) is considered to be in the perfect
#   posture (align in a straight line at 0,0,0)
# * Missing notification of which direction(or axes) being detected
# ----------------------------------------------------------------------------
for pos in range(3):
    if (distPosture[pos] > uprightCheck) and (uprightDetect[pos]):
        if(uprightDetect[3]):
            uprightDetect[3] = False;
            timeNotUpright = time;
            # "==============================="
            # "STATUS: Torso No Longer UPRIGHT"
            # "==============================="
            subj.upright[3] = False;  
        subj.upright[pos] = False;
        
        # Function capturing directions leaving upright position (return as string)
        axisMoved[pos] = find_Direction_Leaving_Upright(currentPosture[pos,0],currentPosture[pos,2]);
        subj.bodyDirectionLeaving[pos] = axisMoved[pos];
        uprightDetect[pos] = False;
        
        

    elif(distPosture[pos] < uprightCheck) and (not uprightDetect[pos]):
        subj.upright[pos] = True;
        subj.bodyDirectionLeaving[pos] = "";
        uprightDetect[pos] = True;
        axisMoved[pos] = "";
        
        if (uprightDetect[0]) and (uprightDetect[1]) and (uprightDetect[2]):
            uprightDetect[3] = True;
            # "============================="
            # "STATUS: Torso Back To UPRIGHT"
            # "============================="
            durationUpright = time - timeNotUpright;
            subj.upright[3] = True;
            subj.addTime(durationUpright,1)
            subj.numNotUpright = subj.numNotUpright + 1;
            notUprightDetect = "";



print(subj)


