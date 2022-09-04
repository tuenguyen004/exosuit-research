
% REQUESTING FOR THESE VALUES:

% time = time passed since recording

% x1 = x of ChestTop
% y1 = y of ChestTop (as in height)
% z1 = z of ChestTop
% originTop = [0,starting y1,0] assuming starting upright

% x2 = x of ChestBot
% y2 = y of ChestBot 
% z2 = z of ChestBot
% originBot = [0,starting y2,0] assuming starting upright

% x3 = x of Tummy
% y3 = y of Tummy
% z3 = z of Tummy
% originTummy = [0,starting y3,0] assuming starting upright

% frontback1 = anterior/posterior of Chest
% leftright1 = lateral of Chest
% rotate1 = rotation of Chest

% frontback2 = anterior/posterior of Hip
% leftright2 = lateral of Hip
% rotate2 = rotation of Hip











% =========================================================================
                  % DETECT VARIABLES FOR STATUS CHECK
% =========================================================================
uprightDetect = [true,true,true,true];  % eachBody (first three logical values) & wholeBody Status Check
straightDetect = [true,true];           % straightback detected already or not, frontView & sideView respectively
straightCompleted = [true,true];        % returned to Straight-Back or not, frontView & sideView respectively

notStraightFrontCounted = false;
notStraightSideCounted = false;

slouchDetect = false;                   % slouching status detect
twistRightDetect = false;              % rotating to right status detect 
twistLeftDetect = false;               % rotating to left status detect 

axisMoved = ["","",""];
notUprightDetect = "";

% =========================================================================
                  % MARGIN OF ERRORS FOR CATEGORIZING
% =========================================================================
uprightCheck = 0.065;                   % Distance each parts must travel before considered not upright 
straightFrontCheck = 5;                 % Back-aligning degree before FrontView not straight
straightSideCheck = 5;                 % Back-aligning degree before SideView not straight

slouchChestCheck = 5;                  % Front/Back angle (in degrees) of Chest before Slouching is detected
slouchHipCheck = -5;                   % Front/Back angle (in degrees) of Hip before Slouching is detected
twistCheck = 15;                       % Degree of Turn before recognized as body rotated

% Time recorded for a new NotStraight = must wait 0.1sec before a Straight signal can be received 
timeFront = 0;                          % FrontView NotStraight Duration
timeSide = 0;                           % FrontView NotStraight Duration
timeSlouch = 0;                         % Slouching Posture Time Duration
timeTwist = 0;
timeNotUpright = 0;











% =====================================================================
% CALCULATE POSITION RELATIVE TO ORIGIN: 
% * currentBot = displaced position (x,y,z) from origins
% * distBot = displaced length (x-z distance) from origins
% * deltaPosture = 3x1 matrix of distances from each origin used for
%   checking if bodypart is no longer within upright position
% * General Direction of Movement = idxTop of ChestTop
% =====================================================================
currentTop = [x1,y1,z1] - originTop;
[maxTopAbs, idxTop] = max(abs(currentTop));
distTop = sqrt(currentTop(1)^2 + currentTop(3)^2);

currentBot = [x2,y2,z2] - originBot;
[maxBotAbs, idxBot] = max(abs(currentBot));
distBot = sqrt(currentBot(1)^2 + currentBot(3)^2);

currentTummy = [x3,y3,z3] - originTummy;
[maxTummyAbs, idxTummy] = max(abs(currentTummy));
distTummy = sqrt(currentTummy(1)^2 + currentTummy(3)^2);

currentPosture = [currentTop;currentBot;currentTummy];
distPosture = [distTop,distBot,distTummy];


% =====================================================================
% CALCULATING ANGLES of FRONT & SIDE-VIEW:
% Breakdown motion into 2D planes: FrontView(x-y) & SideView(y-z) and
%   track angular distance of ChestTop-ChestBottom and ChestBottom-Tummy 
%   and use their angular difference to identify straight back
%   *theta1 = ChestTop to ChestBottom
%   *theta2 = ChestBottom to Tummy
% DECLARING ANGLES OF CHEST & HIP (slouching & direction identifying)
% =====================================================================
thetaFront1 = atan((x1 - x2) / (y1 - y2)) * 180/pi;
thetaFront2 = atan((x2 - x3) / (y2 - y3)) * 180/pi;
diffThetaFront = thetaFront1 - thetaFront2;

thetaSide1 = atan((z1 - z2) / (y1 - y2)) * 180/pi;
thetaSide2 = atan((z2 - z3) / (y2 - y3)) * 180/pi;
diffThetaSide = thetaSide1 - thetaSide2;

aChestFB = frontback1;
aChestLR = leftright1;
aChestRot = rotate1;
aHipFB = frontback2;




                     % ########################
                     % ########################
                     % CATEGORIZING ALGORITHMS: 
                     % ########################
                     % ########################


% =====================================================================
% BACK NOT STRAIGHT SIGNAL = identifying whether or not current positions
%   of ChestTop, ChestBottom, Tummy is aligned with one another
% =====================================================================
if(abs(diffThetaFront) > straightFrontCheck && straightDetect(1))
    timeFront = time;
    straightDetect(1) = false;
    straightCompleted(1) = false;

elseif(abs(diffThetaSide) > straightSideCheck && straightDetect(2))
    timeSide = time;
    straightDetect(2) = false;
    straightCompleted(2) = false;

elseif(abs(diffThetaFront) <= straightFrontCheck && ~straightDetect(1))
    if(time-timeFront > 0.1)
        durationStraight = time - timeFront;
        addTime(subj,durationStraight,2)
        subj.straight = [true,""];

        straightDetect(1) = true;
        straightCompleted(1) = true;
        notStraightFrontCounted = false;
    end

elseif(abs(diffThetaSide) <= straightSideCheck && ~straightDetect(2))
    if(time-timeSide > 0.1)
        durationStraight = time - timeSide;
        addTime(subj,durationStraight,2)
        subj.straight = [true,""];

        straightDetect(2) = true;
        straightCompleted(2) = true;
        notStraightSideCounted = false;
    end
end
% ONLY PUSH OUT THIS MESSAGE IF NOT STRAIGHT FOR ONE FULL SECONDS 
% REPLICATE THE ACTION OF HAPTIC FEEDBACK TO USERS & COUNT STRAIGHTBACK
% THE CODE ABOVE JUST TELL YOU WHEN YOU DON'T HAVE A STRAIGHT BACK FOR
%   RECORD-TRACKING REASONS
if(~straightDetect(1))
    if(time - timeFront > 0.5 && ~notStraightFrontCounted)
       subj.straight = [false,"front"];
       numNotStraightBack = numNotStraightBack + 1;
       subj.numNotStraight = subj.numNotStraight + 1;
       notStraightFrontCounted = true;
    end
end
if(~straightDetect(2))
    if(time - timeSide > 0.5 && ~notStraightSideCounted)
       subj.straight = [false,"side"];
       numNotStraightBack = numNotStraightBack + 1;
       subj.numNotStraight = subj.numNotStraight + 1;
       notStraightSideCounted = true;
    end
end







% =====================================================================
% SLOUCHING SIGNAL = identifying whether current posture is slouching
% =====================================================================
if(aChestFB > slouchChestCheck && aHipFB < slouchHipCheck && ~slouchDetect)
    subj.slouch = true;
    numSlouch = numSlouch + 1;
    subj.numSlouch = subj.numSlouch + 1;
    timeSlouch = time;
    slouchDetect = true;
elseif(aChestFB <= slouchChestCheck && aHipFB >= slouchHipCheck && slouchDetect)
    durationSlouch = time - timeSlouch;
    addTime(subj,durationSlouch,3);
    subj.slouch = false;
    slouchDetect = false;
end











% =====================================================================
% TWISTING SIGNAL = Monitor Body's Rotational Angles to identify
%   rotational motion 
% =====================================================================
if(aChestRot > twistCheck && ~twistLeftDetect)
    subj.twist = [true,"left"];
    subj.numTwist = subj.numTwist + 1;
    numTwist = numTwist + 1;
    timeTwist = time;
    twistLeftDetect = true;
elseif(aChestRot < -twistCheck && ~twistRightDetect)
    subj.twist = [true,"right"];
    subj.numTwist = subj.numTwist + 1;
    numTwist = numTwist + 1;
    timeTwist = time;
    twistRightDetect = true;
elseif(aChestRot >= -twistCheck && aChestRot <= twistCheck && (twistLeftDetect || twistRightDetect))
    durationTwist = time - timeTwist;
    addTime(subj,durationTwist,4)
    subj.twist = [false,""];
    twistLeftDetect = false;
    twistRightDetect = false;
end






% =====================================================================
% DIRECTION WHILE NOTUPRIGHT SIGNAL = where body located/tilting or not 
%   once outside upright zone & tracking movement outside upright based
%   on body's angles not actual position (can track position by looking
%   at the body coordinates)
% Upright Detection is based on whether CHESTTOP is upright or not ONLY
% =====================================================================
test = find_Motion_NotUpright(aChestFB,aChestLR);
if(~uprightDetect(1) && test ~= notUprightDetect && test ~= "")
    notUprightDetect = test;
    subj.notUprightDirection = test;
end








% =====================================================================
% UPRIGHT SIGNAL = original upright posture where all three positions
%   (ChestTop, ChestBottom, Tummy) is considered to be in the perfect
%   posture (align in a straight line at 0,0,0)
% * Missing notification of which direction(or axes) being detected
% =====================================================================
for pos=1:3
    if(distPosture(pos) > uprightCheck && uprightDetect(pos))
        if(uprightDetect(4))
            uprightDetect(4) = false;
            numNotUpright = numNotUpright + 1;
            subj.numNotUpright = subj.numNotUpright + 1;
            timeNotUpright = time;
            subj.upright(4) = false;  
        end
        subj.upright(pos) = false;

        % Function capturing directions leaving upright position (return as string)
        axisMoved(pos) = find_Direction_Leaving_Upright(currentPosture(pos,1),currentPosture(pos,3));
        disp(string(currentPosture(pos,:)))
        subj.bodyDirectionLeaving(pos) = axisMoved(pos);
        uprightDetect(pos) = false;



    elseif(distPosture(pos) < uprightCheck && ~uprightDetect(pos))
        subj.upright(pos) = true;
        disp(string(currentPosture(pos,:)))
        subj.bodyDirectionLeaving(pos) = "";
        uprightDetect(pos) = true;
        axisMoved(pos) = "";

        if(uprightDetect(1) && uprightDetect(2) && uprightDetect(3))
            uprightDetect(4) = true;
            durationUpright = time - timeNotUpright;
            subj.upright(4) = true;
            addTime(subj,durationUpright,1)
            notUprightDetect = "";
        end
    end 
end

    

