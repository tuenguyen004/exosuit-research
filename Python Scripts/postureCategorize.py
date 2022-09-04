""" --------------------------
POSTURE-CATEGORIZING ALGORITHM
------------------------------
     > Created from Early July 2020 by Tue Nguyen'23
     > Taken from MATLAB and transfered into Python
 
    
CHANGES:
    > Removed all Visualization Plots Feature from MATLAB 
    > Visualization of Angles of Chest/Hip can be done BUT not priority
    > Counter variable now iterate after (old: before) movement completion 
    
LIMITATIONS:
    > margins of error must be CALIBRATED for accurate classification
    > notStraightBack only reported signal after sustained for 1 sec
    > notUpright Direction only track based on tilting Chest_Angles and only 
        get triggered once ChestTop is out of error margin 
    
    

    
"""
import math
import numpy as np
import pandas as pd

# pandas.Dataframe element indexing ==> df.iloc[row,col]
# pandas.Dataframe extract columns  ==> df.iloc[:,0]
# pandas.Dataframe extract rows     ==> df.iloc[0,:]

# IMPORTANT to adjust if transfer to new destination
root = "C:\\Users\\tueng\\Documents\\Tufts Research"


# ============================================================================
# ====================== PRE-DEFINED BASIC FUNCTIONS =========================
#  Taken from SpikeDetectionV2.ipynb (credits to Tufts Exosuit Research Team)
# ============================================================================

# read in .csv file and return pd.DataFrame
def findPath(folder, filename):
    data = pd.DataFrame()
    data = pd.read_csv(root + folder + "\\" + filename, index_col=False)
    return data


def find_Motion_NotUpright(frontBack, leftRight):
    xStatus = ""
    zStatus = ""
    direction = ""

    # determining if X and/or Z direction are negative
    # NOTE: right(+) and left(-) for tilting angle
    if leftRight > 10:
        xStatus = "X-"
    elif leftRight < -10:
        xStatus = "X"

    if frontBack > 0:
        zStatus = "Z"
    elif frontBack < 0:
        zStatus = "Z-"

    absLR = abs(leftRight)
    absFB = abs(frontBack)
    # determine the strength of each direction & finalize in a string variable
    if absFB > 12 and absLR < 12:
        direction = zStatus
    elif absFB < 12 and absLR > 12:
        direction = xStatus
    elif absFB > 12 and absLR > 12:
        if absLR > absFB:
            direction = xStatus + " " + zStatus
        elif absLR < absFB:
            direction = zStatus + " " + xStatus
        else:
            direction = xStatus + " = " + zStatus

    return direction


def find_Direction_Leaving_Upright(x, z):
    # Return a string of which direction(s) the object is leaving upright

    diff = abs(x) - abs(z)
    motionCheck = (
        0.02  # Threshold of x & z position before considered the presence of that
    )
    #   axis in the object's motion
    diffXZ = 0.03  # Threshold of x & z position before considered the presence of that
    #   axis RELATIVE TO EACH OTHER in the object's motion
    output = ""

    if (abs(x) > motionCheck) or (abs(z) > motionCheck):
        if (diff > 0) and (abs(diff) > diffXZ):
            output = "X"
            if x < 0:
                output = output + "-"

        elif (diff < 0) and (abs(diff) > diffXZ):
            output = "Z"
            if z < 0:
                output = output + "-"

        elif (diff > 0) and (abs(diff) <= diffXZ):
            output = "X Z"
            if x < 0 and z < 0:
                output = "X- Z-"
            elif x < 0 and z > 0:
                output = "X- Z"
            elif x > 0 and z < 0:
                output = "X Z-"

        elif (diff < 0) and (abs(diff) <= diffXZ):
            output = "Z X"
            if x < 0 and z < 0:
                output = "Z- X-"
            elif x < 0 and z > 0:
                output = "Z X-"
            elif x > 0 and z < 0:
                output = "Z- X"
    return output


# ============================================================================
# ====================== POSTURE() CLASS DECLARATION =========================
# ============================================================================

# Posture() Object Class for Real-time Classification of the Subject's Posture
class Posture:
    # Default Constructor when object first call
    def __init__(self):
        self.upright = np.array([True, True, True, True])
        self.straightFront = True
        self.straightSide = True
        self.slouch = False
        self.twist = [False, ""]

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

        self.bodyDirectionLeaving = np.array(["", "", ""])
        self.notUprightDirection = ""

    # Adding Time Duration to Specific Category
    # 1 = notUpright
    # 2 = notStraight
    # 3 = slouching
    # 4 = twisting
    def addTime(self, timeDuration, idTest):
        if idTest == 1:
            self.notUprightTime.append(timeDuration)
        elif idTest == 2:
            if not self.straightFront:
                self.notStraightTime_Front.append(timeDuration)
            elif not self.straightSide:
                self.notStraightTime_Side.append(timeDuration)
        elif idTest == 3:
            self.slouchTime.append(timeDuration)
        elif idTest == 4:
            if self.twist[1] == "left":
                self.twistTime_Left.append(timeDuration)
            elif self.twist[1] == "right":
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
        print("              notUprightTime: " + str(self.notUprightTime))
        print("       notStraightTime_Front: " + str(self.notStraightTime_Front))
        print("        notStraightTime_Side: " + str(self.notStraightTime_Side))
        print("                  slouchTime: " + str(self.slouchTime))
        print("              twistTime_Left: " + str(self.twistTime_Left))
        print("             twistTime_Right: " + str(self.twistTime_Right))
        print("")

        return ""


# ============================================================================
# ==================== IMPORTING DATAFILES INTO PYTHON ======================
# ============================================================================
study2A = np.array(
    [
        "PilotStudy 2A (Curve Back)\Trial 1 9.34pm",
        "PilotStudy 2A (Curve Back)\Trial 2 9.35pm",
        "PilotStudy 2A (Curve Back)\Trial 3 9.36pm",
        "PilotStudy 2A (Curve Back)\Trial 4 9.38pm",
        "PilotStudy 2A (Curve Back)\Trial 5 9.40pm",
    ]
)
study2B = np.array(
    [
        "PilotStudy 2B (Straight Back)\Trial 1 9.42pm",
        "PilotStudy 2B (Straight Back)\Trial 2 9.47pm",
        "PilotStudy 2B (Straight Back)\Trial 3 9.48pm",
        "PilotStudy 2B (Straight Back)\Trial 4 9.49pm",
        "PilotStudy 2B (Straight Back)\Trial 5 9.53pm",
    ]
)
study2C = np.array(
    [
        "PilotStudy 2C (Side Bend)\Trial 1 9.54pm",
        "PilotStudy 2C (Side Bend)\Trial 2 9.55pm",
        "PilotStudy 2C (Side Bend)\Trial 3 9.58pm",
    ]
)
study2D = np.array(
    [
        "PilotStudy 2D (Side Twist)\Trial 1 10.02pm",
        "PilotStudy 2D (Side Twist)\Trial 2 10.03pm",
        "PilotStudy 2D (Side Twist)\Trial 3 10.04pm",
    ]
)
study2E = np.array(
    [
        "PilotStudy 2E (Slouching)\Trial 1 10.06pm",
        "PilotStudy 2E (Slouching)\Trial 2 10.07pm",
        "PilotStudy 2E (Slouching)\Trial 3 10.08pm",
    ]
)

# IMPORTANT to adjust if targetting specific trials
# june11 = "\\Data_PilotStudy June11\\" + study2A[2]
june11 = "\\Data_PilotStudy July31\Trial 1\\"
june20 = "\\Data_PilotStudy June20\\"

t1 = findPath(june11, "Positions_ChestTop.csv")
t2 = findPath(june11, "Positions_ChestBottom.csv")
t3 = findPath(june11, "Positions_Tummy.csv")
t4 = findPath(june11, "Angles_Chest.csv")
t5 = findPath(june11, "Angles_Hip.csv")


# ============================================================================
# ====================== GLOBAL CONSTANTS DECLARATION ========================
# ============================================================================
totalLength = t1.index[-1]
axisIndex = np.array(["X", "Y", "Z"])
skeleton = np.array(["ChestTop", "ChestBot", "Tummy"])

# ----------------------------------------------------------------------------
# ----------------------- Variables for STATUS CHECK -------------------------
# ----------------------------------------------------------------------------
uprightDetect = np.array(
    [True, True, True, True]
)  # eachBody (first three logical values) & wholeBody Status Check
straightDetect = np.array(
    [True, True]
)  # straightback detected already or not, frontView & sideView
straightCompleted = np.array(
    [True, True]
)  # returned to Straight-Back or not, frontView & sideView

slouchDetect = False  # slouching status detect
twistRightDetect = False  # rotating to right status detect
twistLeftDetect = False  # rotating to left status detect

notStraightFrontCounted = False
notStraightSideCounted = False

axisMoved = np.array(["", "", ""])
notUprightDetect = ""
# ----------------------------------------------------------------------------
# --------------------- MARGIN OF ERRORS for Categorizing --------------------
# ----------------------------------------------------------------------------
uprightCheck = 0.065  # Distance each parts must travel before considered not upright
straightFrontCheck = 5  # Back-aligning degree before FrontView not straight
straightSideCheck = 10  # Back-aligning degree before SideView not straight

slouchChestCheck = (
    5  # Front/Back angle (in degrees) of Chest before Slouching is detected
)
slouchHipCheck = -5  # Front/Back angle (in degrees) of Hip before Slouching is detected
twistCheck = 15  # Degree of Turn before recognized as body rotated

# Time recorded for a new NotStraight = must wait 0.1sec before a Straight signal can be received
timeFront = 0
timeSide = 0
timeSlouch = 0
timeTwist = 0
timeNotUpright = 0


# ============================================================================
# ===================== DATAFILES PRE-ANALYSIS PREPARATION ===================
# ============================================================================

# Time Duration (assumed all datafiles have the same # values as Position_ChestTop)
time = t1.iloc[:, 0]

# Positions_ChestTop
x1 = t1.iloc[:, 1]
y1 = t1.iloc[:, 2]
z1 = t1.iloc[:, 3]

# Positions_ChestBottom
x2 = t2.iloc[:, 1]
y2 = t2.iloc[:, 2]
z2 = t2.iloc[:, 3]

# Positions_Tummy
x3 = t3.iloc[:, 1]
y3 = t3.iloc[:, 2]
z3 = t3.iloc[:, 3]

# Angles_Chest
frontback1 = t4.iloc[:, 1]
leftright1 = t4.iloc[:, 2]
rotate1 = t4.iloc[:, 3]

# Angles_Hip
frontback2 = t5.iloc[:, 1]
leftright2 = t5.iloc[:, 2]
rotate2 = t5.iloc[:, 3]

# ----------------------------------------------------------------------------
# --------------------------- FOR-LOOP SETTINGS ------------------------------
# ----------------------------------------------------------------------------
originTop = np.array([0, y1[0], 0])
# ChestTop Origin
originBot = np.array([0, y2[0], 0])
# ChestBottom Origin
originTummy = np.array([0, y3[0], 0])
# Tummy Origin

# Initiate 'subj' to hold posture-categorizing data
subj = Posture()

start = 0
step = 1
stop = totalLength

# Variable to store labeled ChestTop Positions
label_Upright = []
label_Straight = []
label_Twist = []
label_Slouch = []


for i in range(start, stop + 1, step):
    # ----------------------------------------------------------------------------
    # ------------- Positional Calculation (distance & axis index) ---------------
    # ----------------------------------------------------------------------------
    currentTop = np.array([x1[i], y1[i], z1[i]]) - originTop
    maxTopAbs = max(abs(currentTop))
    idxTop = np.argmax(abs(currentTop))
    distTop = math.sqrt(currentTop[0] ** 2 + currentTop[2] ** 2)

    currentBot = np.array([x2[i], y2[i], z2[i]]) - originBot
    maxBotAbs = max(abs(currentBot))
    idxBot = np.argmax(abs(currentBot))
    distBot = math.sqrt(currentBot[0] ** 2 + currentBot[2] ** 2)

    currentTummy = np.array([x3[i], y3[i], z3[i]]) - originTummy
    maxTummyAbs = max(abs(currentTummy))
    idxTummy = np.argmax(abs(currentTummy))
    distTummy = math.sqrt(currentTummy[0] ** 2 + currentTummy[2] ** 2)

    currentPosture = np.array([currentTop, currentBot, currentTummy])
    distPosture = np.array([distTop, distBot, distTummy])

    # ----------------------------------------------------------------------------
    # ------ Angular Calculation (theta derivation of frontView & sideView) ------
    # ----------------------------------------------------------------------------
    radianToDegree = 180 / np.pi

    thetaFront1 = math.atan((x1[i] - x2[i]) / (y1[i] - y2[i])) * radianToDegree
    thetaFront2 = math.atan((x2[i] - x3[i]) / (y2[i] - y3[i])) * radianToDegree
    diffThetaFront = thetaFront1 - thetaFront2

    # print(diffThetaFront)
    # print("\n")

    thetaSide1 = math.atan((z1[i] - z2[i]) / (y1[i] - y2[i])) * radianToDegree
    thetaSide2 = math.atan((z2[i] - z3[i]) / (y2[i] - y3[i])) * radianToDegree
    diffThetaSide = thetaSide1 - thetaSide2

    aChestFB = frontback1[i]
    aChestLR = leftright1[i]
    aChestRot = rotate1[i]
    aHipFB = frontback2[i]

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
        timeFront = time[i]
        straightDetect[0] = False
        straightCompleted[0] = False

    # ***** SIDE VIEW: BACK NOT STRAIGHT *****
    elif (abs(diffThetaSide) > straightSideCheck) and (straightDetect[1]):
        straightCompleted[1] = False

        timeSide = time[i]
        straightDetect[1] = False
    # ***** FRONT VIEW: RETURNED TO STRAIGHT *****
    elif (abs(diffThetaFront) <= straightFrontCheck) and (not straightDetect[0]):
        if time[i] - timeFront > 0.1:
            durationStraight = time[i] - timeFront
            subj.addTime(durationStraight, 2)
            subj.straightFront = True
            straightDetect[0] = True
            straightCompleted[0] = True
            notStraightFrontCounted = False

    # ***** SIDE VIEW: RETURNED TO STRAIGHT *****
    elif (abs(diffThetaSide) <= straightSideCheck) and (not straightDetect[1]):
        if time[i] - timeSide > 0.1:
            durationStraight = time[i] - timeSide
            subj.addTime(durationStraight, 2)
            subj.straightSide = True
            straightDetect[1] = True
            straightCompleted[1] = True
            notStraightSideCounted = False

    # ----------------------------------------------------------------------------
    # > Only after one second, send out backNotStraight signal & save that status
    #   into Posture() class ==> otherwise don't do anything
    # ----------------------------------------------------------------------------
    # ***** frontView: back not straight for 1 second *****
    if not straightDetect[0]:
        if (time[i] - timeFront > 0.5) and (not notStraightFrontCounted):
            subj.straightFront = False
            subj.numNotStraight = subj.numNotStraight + 1
            notStraightFrontCounted = True

    # ***** sideView: back not straight for 1 second *****
    if not straightDetect[1]:
        if (time[i] - timeSide > 0.5) and (not notStraightSideCounted):
            subj.straightSide = False
            subj.numNotStraight = subj.numNotStraight + 1
            notStraightSideCounted = True

    # ----------------------------------------------------------------------------
    # > SLOUCHING SIGNAL = identifying whether current posture is "slouching"
    #
    # > Checking for a positive Chest_Angle and a negative Hip_Angle
    # ----------------------------------------------------------------------------
    # ***** Posture Slouching *****
    if (
        (aChestFB > slouchChestCheck)
        and (aHipFB < slouchHipCheck)
        and (not slouchDetect)
    ):
        subj.slouch = True
        timeSlouch = time[i]
        slouchDetect = True
    # ***** Posture Not Slouching *****
    elif (
        (aChestFB <= slouchChestCheck) and (aHipFB >= slouchHipCheck) and (slouchDetect)
    ):
        durationSlouch = time[i] - timeSlouch
        subj.addTime(durationSlouch, 3)
        subj.numSlouch = subj.numSlouch + 1
        subj.slouch = False
        slouchDetect = False

    # ----------------------------------------------------------------------------
    # > TWISTING SIGNAL = identifying by checking Chest's rotation
    #
    # > Checking for a left/right rotational Chest_Angle
    # ----------------------------------------------------------------------------
    if (aChestRot > twistCheck) and (not twistLeftDetect):
        subj.twist = [True, "left"]
        timeTwist = time[i]
        twistLeftDetect = True
    elif (aChestRot < -twistCheck) and (not twistRightDetect):
        subj.twist = [True, "right"]
        timeTwist = time[i]
        twistRightDetect = True
    elif (
        (aChestRot >= -twistCheck)
        and (aChestRot <= twistCheck)
        and (twistLeftDetect or twistRightDetect)
    ):
        durationTwist = time[i] - timeTwist
        subj.addTime(durationTwist, 4)
        subj.numTwist = subj.numTwist + 1
        subj.twist = [False, ""]
        twistLeftDetect = False
        twistRightDetect = False

    # ----------------------------------------------------------------------------
    # NOTUPRIGHT DIRECTION SIGNAL = where body located/tilting or not
    #   once outside upright zone & tracking movement outside upright based
    #   on body's angles not actual position (can track position by looking
    #   at the body coordinates)
    # Upright Detection is based on whether CHESTTOP is upright or not ONLY
    # ----------------------------------------------------------------------------
    direct = find_Motion_NotUpright(aChestFB, aChestLR)
    if (not uprightDetect[0]) and (direct != notUprightDetect) and (direct != ""):
        notUprightDetect = direct
        subj.notUprightDirection = direct

    # ----------------------------------------------------------------------------
    # UPRIGHT SIGNAL = original upright posture where all three positions
    #   (ChestTop, ChestBottom, Tummy) is considered to be in the perfect
    #   posture (align in a straight line at 0,0,0)
    # * Missing notification of which direction(or axes) being detected
    # ----------------------------------------------------------------------------
    for pos in range(3):
        if (distPosture[pos] > uprightCheck) and (uprightDetect[pos]):
            if uprightDetect[3]:
                uprightDetect[3] = False
                timeNotUpright = time[i]
                # "==============================="
                # "STATUS: Torso No Longer UPRIGHT"
                # "==============================="
                subj.upright[3] = False
            subj.upright[pos] = False

            # Function capturing directions leaving upright position (return as string)
            axisMoved[pos] = find_Direction_Leaving_Upright(
                currentPosture[pos, 0], currentPosture[pos, 2]
            )
            subj.bodyDirectionLeaving[pos] = axisMoved[pos]
            uprightDetect[pos] = False

        elif (distPosture[pos] < uprightCheck) and (not uprightDetect[pos]):
            subj.upright[pos] = True
            subj.bodyDirectionLeaving[pos] = ""
            uprightDetect[pos] = True
            axisMoved[pos] = ""

            if (uprightDetect[0]) and (uprightDetect[1]) and (uprightDetect[2]):
                uprightDetect[3] = True
                # "============================="
                # "STATUS: Torso Back To UPRIGHT"
                # "============================="
                durationUpright = time[i] - timeNotUpright
                subj.upright[3] = True
                subj.addTime(durationUpright, 1)
                subj.numNotUpright = subj.numNotUpright + 1
                notUprightDetect = ""

    # ----------------------------------------------------------------------------
    # MAKING LABELLED DATA OF SPECIFIC FEATURE FOR MACHINE LEARNING
    # ----------------------------------------------------------------------------
    # Positions_ChestTop

    # label_ChestTop.append(subj.upright[0])
    # label_ChestTop.append(subj.upright[0])

    uprightStatus = []
    # ChestTop
    if subj.upright[0]:
        uprightStatus.append(1)
    else:
        uprightStatus.append(0)
    # ChestBot
    if subj.upright[1]:
        uprightStatus.append(1)
    else:
        uprightStatus.append(0)
    # Tummy
    if subj.upright[2]:
        uprightStatus.append(1)
    else:
        uprightStatus.append(0)
    # wholeTorso
    if subj.upright[3]:
        uprightStatus.append(1)
    else:
        uprightStatus.append(0)
    label_Upright.append(uprightStatus)

    # [frontView, sideView]
    straightStatus = []
    if subj.straightFront:
        straightStatus.append(1)
    elif not subj.straightFront:
        straightStatus.append(0)

    if subj.straightSide:
        straightStatus.append(1)
    elif not subj.straightSide:
        straightStatus.append(0)
    label_Straight.append(straightStatus)

    # [left, right]
    twistStatus = []
    if subj.twist[0]:
        if subj.twist[1] == "left":
            twistStatus.append(1)
            twistStatus.append(0)
        elif subj.twist[1] == "right":
            twistStatus.append(0)
            twistStatus.append(1)
    else:
        twistStatus.append(0)
        twistStatus.append(0)
    label_Twist.append(twistStatus)

    slouchStatus = []
    if subj.slouch:
        slouchStatus.append(1)
    else:
        slouchStatus.append(0)
    label_Slouch.append(slouchStatus)


# ============================================================================
# ============================ ENDING OUTPUTS ================================
# ============================================================================

# Printing Out Status of Current User's Posture
print(subj)
# print(len(label_Straight))
print(label_Twist)


userInput = input("Convert to CSV file?\n y = yes, anything else = no\n")
if userInput == "y":
    df = pd.DataFrame(label_Twist)
    CSVname = "WilliamJuly31 - Trial1 - Twist.csv"
    df.to_csv(root + "\\Data_Labelled\\" + CSVname)