clear;
close all;
clc;

study2A = ["PilotStudy 2A (Curve Back)\Trial 1 9.34pm",...
           "PilotStudy 2A (Curve Back)\Trial 2 9.35pm",...
           "PilotStudy 2A (Curve Back)\Trial 3 9.36pm",...
           "PilotStudy 2A (Curve Back)\Trial 4 9.38pm",...
           "PilotStudy 2A (Curve Back)\Trial 5 9.40pm"];
study2B = ["PilotStudy 2B (Straight Back)\Trial 1 9.42pm",...
           "PilotStudy 2B (Straight Back)\Trial 2 9.47pm",...
           "PilotStudy 2B (Straight Back)\Trial 3 9.48pm",...
           "PilotStudy 2B (Straight Back)\Trial 4 9.49pm",...
           "PilotStudy 2B (Straight Back)\Trial 5 9.53pm"];
study2C = ["PilotStudy 2C (Side Bend)\Trial 1 9.54pm",...
           "PilotStudy 2C (Side Bend)\Trial 2 9.55pm",...
           "PilotStudy 2C (Side Bend)\Trial 3 9.58pm"]; 
study2D = ["PilotStudy 2D (Side Twist)\Trial 1 10.02pm",...
           "PilotStudy 2D (Side Twist)\Trial 2 10.03pm",...
           "PilotStudy 2D (Side Twist)\Trial 3 10.04pm"]; 
study2E = ["PilotStudy 2E (Slouching)\Trial 1 10.06pm",...
           "PilotStudy 2E (Slouching)\Trial 2 10.07pm",...
           "PilotStudy 2E (Slouching)\Trial 3 10.08pm"]; 
% =========================================================================
                    % import DATAFILES into MATLAB
% =========================================================================
% Adjust root folder as needed
root = "C:\Users\tueng\Documents\Tufts\Tufts Exosuit_ML\";
folder = "\Data_PilotStudy June11\";
folder2 = "\Data_PilotStudy June20";
folder3 = "\Data_PilotStudy July6\Trial 2";
folder4 = "\Data_PilotStudy July20\Trial 2";
folder4 = "\Data_PilotStudy July31\Trial 2";
folder5 = "\Data_James Dec31";
folder5 = "\Data_James Jan6";
folder6 = "\Data_Gordon";
addpath(root + folder3)

t1 = readtable('Positions_ChestTop.csv');
t2 = readtable('Positions_ChestBottom.csv');
t3 = readtable('Positions_Tummy.csv');
t4 = readtable('Angles_Chest.csv');
t5 = readtable('Angles_Hip.csv');





% =========================================================================
                     % GLOBAL CONSTANT DECLARATION
% =========================================================================
totalLength = height(t1);       
axisIndex = ["X","Y","Z"];
skeleton = ["ChestTop","ChestBot","Tummy"];

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

% =========================================================================
                      % POSTURE CATEGORY COUNTERS
% =========================================================================
numNotUpright = 0;              % Number of times NOT UPRIGHT SIGNAL is detected 
numNotStraightBack = 0;         % Number of times BACK NOT STRAIGHT SIGNAL is detected  
numSlouch = 0;                  % Number of times SLOUCHING SIGNAL is detected
numTwist = 0;                   % Number of times TWIST SIGNAL is detected











% =========================================================================
              % EXTRACT DATA into ARRAYS: ChestTop Positions     
% =========================================================================
sample1 = head(t1, totalLength);     
Pos_Data1 = table2array(sample1(:,1:4));
time = Pos_Data1(:,1);
z1 = Pos_Data1(:,4);     
y1 = Pos_Data1(:,3);     
x1 = Pos_Data1(:,2);     
% =========================================================================
             % EXTRACT DATA into ARRAYS: ChestBottom Positions
% =========================================================================
sample2 = head(t2, totalLength);           
Pos_Data2 = table2array(sample2(:,1:4));
z2 = Pos_Data2(:,4);
y2 = Pos_Data2(:,3);
x2 = Pos_Data2(:,2);
% =========================================================================
                % EXTRACT DATA into ARRAYS: Tummy Positions
% =========================================================================
sample3 = head(t3, totalLength);           
Pos_Data3 = table2array(sample3(:,1:4));
z3 = Pos_Data3(:,4);
y3 = Pos_Data3(:,3);
x3 = Pos_Data3(:,2);
% =========================================================================
                 % EXTRACT DATA into ARRAYS: Chest Angles
% =========================================================================
sample4 = head(t4, totalLength);           
Angle_Data1 = table2array(sample4(:,1:4));
rotate1 = Angle_Data1(:,4);
leftright1 = Angle_Data1(:,3);
frontback1 = Angle_Data1(:,2);
% =========================================================================
                   % EXTRACT DATA into ARRAYS: Hip Angles
% =========================================================================
sample5 = head(t5, totalLength);           
Angle_Data2 = table2array(sample5(:,1:4));
rotate2 = Angle_Data2(:,4);
leftright2 = Angle_Data2(:,3);
frontback2 = Angle_Data2(:,2);










% =========================================================================
                   % 'lEt'S mAkE gRaPh BeAuTiFuL' SETTINGS
% =========================================================================
curve1 = animatedline('LineWidth',2,'Color','r');   %ChestTop = Red
curve2 = animatedline('LineWidth',2,'Color','b');   %ChestBottom = Blue
curve3 = animatedline('LineWidth',2,'Color','g');   %Tummy = Green
set(gca, 'XLim',[-0.5 0.5],'YLim',[-0.5 0.5],'ZLim',[-0.25 0.75]);
    %Visualization Graph Dimension: (need subject's anthropometric data)
    %Xlim = left/right          (side)
    %Ylim = forward/backward    (depth)
    %Zlim = up/down             (height)
    %set(gca, 'XLim',[min(x1) max(x1)],'YLim',[min(y1) max(y1)],'ZLim',[min(z1) max(z1)]);
set(gca, 'Xdir', 'reverse')     % Revert x-axis to represent left and right visualization
set(gca,'FontSize',7)
grid on;
hold on;
xlabel('right(-) | left(+)');
ylabel('front(+) | back(-)');
zlabel('down(-) | up(+)');
legend('ChestTop','ChestBottom','Tummy')








% =========================================================================
                    % POINT-OF-VIEW & @ 0seconds SETTING    
% =========================================================================
    view(180,90);              % Top View
    %view(-180,0);              % Front View
    %view(-90,1);                % Side View
originTop = [0,y1(1),0];        % ChestTop Origin
originBot = [0,y2(1),0];        % ChestBottom Origin
originTummy = [0,y3(1),0];      % Tummy Origin
             
start = 1;                  
step = 10;               % For sample down (potentially use linspace?) 
stop = totalLength;              % totalLength (max array index = 53999)



                    
                    

subj = Posture();


% =========================================================================
         % VISUALIZATION & ANALYSIS: ChestTop, ChestBottom, Tummy
% =========================================================================
for i=start:step:stop
    % =====================================================================
    % GRAPH POSITION: currently ChestBottom, ChestTop, Tummy  
    % when graph, MATLAB Y-Axis (Front/Back) use Z-Axis Data instead
    % =====================================================================
    addpoints(curve1,x1(i),z1(i),y1(i));
    head1 = scatter3(x1(i),z1(i),y1(i));
    addpoints(curve2,x2(i),z2(i),y2(i));
    head2 = scatter3(x2(i),z2(i),y2(i));
    addpoints(curve3,x3(i),z3(i),y3(i));
    head3 = scatter3(x3(i),z3(i),y3(i));
    drawnow;
    %pause(0.1)
    if(i ~= stop) 
        delete(head1)
        delete(head2)
        delete(head3)
    end
    
    if(mod(time(i),300) == 0)
       disp("            time passed: " + string(time(i)/60 + " minutes")); 
    end
    
    % =====================================================================
    % CALCULATE POSITION RELATIVE TO ORIGIN: 
    % * currentBot = displaced position (x,y,z) from origins
    % * distBot = displaced length (x-z distance) from origins
    % * deltaPosture = 3x1 matrix of distances from each origin used for
    %   checking if bodypart is no longer within upright position
    % * General Direction of Movement = idxTop of ChestTop
    % =====================================================================
    currentTop = [x1(i),y1(i),z1(i)] - originTop;
    [maxTopAbs, idxTop] = max(abs(currentTop));
    distTop = sqrt(currentTop(1)^2 + currentTop(3)^2);
    
    currentBot = [x2(i),y2(i),z2(i)] - originBot;
    [maxBotAbs, idxBot] = max(abs(currentBot));
    distBot = sqrt(currentBot(1)^2 + currentBot(3)^2);
    
    currentTummy = [x3(i),y3(i),z3(i)] - originTummy;
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
    thetaFront1 = atan((x1(i) - x2(i)) / (y1(i) - y2(i))) * 180/pi;
    thetaFront2 = atan((x2(i) - x3(i)) / (y2(i) - y3(i))) * 180/pi;
    diffThetaFront = thetaFront1 - thetaFront2;
    
    thetaSide1 = atan((z1(i) - z2(i)) / (y1(i) - y2(i))) * 180/pi;
    thetaSide2 = atan((z2(i) - z3(i)) / (y2(i) - y3(i))) * 180/pi;
    diffThetaSide = thetaSide1 - thetaSide2;
    
    aChestFB = frontback1(i);
    aChestLR = leftright1(i);
    aChestRot = rotate1(i);
    aHipFB = frontback2(i);
    

    

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
        disp("***** FRONT VIEW: BACK NOT STRAIGHT! @" + string(time(i)) + "sec *****");
        disp(" ");
        timeFront = time(i);
        straightDetect(1) = false;
        straightCompleted(1) = false;
        
    elseif(abs(diffThetaSide) > straightSideCheck && straightDetect(2))
        disp("***** SIDE VIEW: BACK NOT STRAIGHT!! @" + string(time(i)) + "sec *****");
        disp(" ")
        timeSide = time(i);
        straightDetect(2) = false;
        straightCompleted(2) = false;
           
    elseif(abs(diffThetaFront) <= straightFrontCheck && ~straightDetect(1))
        if(time(i)-timeFront > 0.1)
            disp("***** FRONT VIEW: RETURNED TO STRAIGHT @" + string(time(i)) + "sec *****");
            disp("  *** Time Duration: " + string(time(i) - timeFront) + "sec ***");
            disp(" ")
            durationStraight = time(i) - timeFront;
            addTime(subj,durationStraight,2)
            subj.straight = [true,""];
            
            straightDetect(1) = true;
            straightCompleted(1) = true;
            notStraightFrontCounted = false;
        end
        
    elseif(abs(diffThetaSide) <= straightSideCheck && ~straightDetect(2))
        if(time(i)-timeSide > 0.1)
            disp("***** SIDE VIEW: RETURNED TO STRAIGHT @" + string(time(i)) + "sec *****");
            disp("  *** Time Duration: " + string(time(i) - timeSide) + "sec ***");
            disp(" ")
            durationStraight = time(i) - timeSide;
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
        if(time(i) - timeFront > 0.5 && ~notStraightFrontCounted)
           disp("frontView: back not straight for 1 second") 
           disp(" ")
           subj.straight = [false,"front"];
           numNotStraightBack = numNotStraightBack + 1;
           subj.numNotStraight = subj.numNotStraight + 1;
           notStraightFrontCounted = true;
        end
    end
    if(~straightDetect(2))
        if(time(i) - timeSide > 0.5 && ~notStraightSideCounted)
           disp("sideView: back not straight for 1 second") 
           disp(" ")
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
        disp("     ..... POSTURE SLOUCHING @" + string(time(i)) + "sec .....");
        disp(' ')
        subj.slouch = true;
        numSlouch = numSlouch + 1;
        subj.numSlouch = subj.numSlouch + 1;
        timeSlouch = time(i);
        slouchDetect = true;
    elseif(aChestFB <= slouchChestCheck && aHipFB >= slouchHipCheck && slouchDetect)
        disp("     ..... POSTURE NOT SLOUCHING @" + string(time(i)) + "sec .....");
        disp("       ..... Time Duration: " + string(time(i) - timeSlouch) + "sec ....");
        disp(' ')
        durationSlouch = time(i) - timeSlouch;
        addTime(subj,durationSlouch,3);
        subj.slouch = false;
        slouchDetect = false;
    end
    
    
    
    
    
    
    
    
    
    
    
    % =====================================================================
    % TWISTING SIGNAL = Monitor Body's Rotational Angles to identify
    %   rotational motion 
    % =====================================================================
    if(aChestRot > twistCheck && ~twistLeftDetect)
        disp("     <<<<< TWISTED to LEFT @" + string(time(i)) + "sec >>>>>")
        disp("     <<<<< TWISTED to LEFT @" + string(time(i)) + "sec >>>>>")
        disp("     <<<<< TWISTED to LEFT @" + string(time(i)) + "sec >>>>>")
        disp(" ")
        subj.twist = [true,"left"];
        subj.numTwist = subj.numTwist + 1;
        numTwist = numTwist + 1;
        timeTwist = time(i);
        twistLeftDetect = true;
    elseif(aChestRot < -twistCheck && ~twistRightDetect)
        disp("     <<<<< TWISTED to RIGHT @" + string(time(i)) + "sec >>>>>")
        disp("     <<<<< TWISTED to RIGHT @" + string(time(i)) + "sec >>>>>")
        disp("     <<<<< TWISTED to RIGHT @" + string(time(i)) + "sec >>>>>")
        disp(" ")
        subj.twist = [true,"right"];
        subj.numTwist = subj.numTwist + 1;
        numTwist = numTwist + 1;
        timeTwist = time(i);
        twistRightDetect = true;
    elseif(aChestRot >= -twistCheck && aChestRot <= twistCheck && (twistLeftDetect || twistRightDetect))
        disp("     <<<<< not twisting @" + string(time(i)) + "sec >>>>>")
        disp("     <<<<< Time Duration: " + string(time(i) - timeTwist) + "sec >>>>>");
        disp(" ")
        durationTwist = time(i) - timeTwist;
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
        disp("     ^^^^^ NotUpright Direction is " + test + " ^^^^^");
        disp("     ^^^^^ NotUpright Direction is " + test + " ^^^^^");
        disp("     ^^^^^ NotUpright Direction is " + test + " ^^^^^");
        disp(' ');
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
                timeNotUpright = time(i);
                disp("===============================")
                disp("STATUS: Torso No Longer UPRIGHT ==> " + string(time(i)) + "sec")
                disp("===============================")
                subj.upright(4) = false;  
            end
            disp(skeleton(pos) + " OUT @" + string(time(i)) + "sec");
            subj.upright(pos) = false;
            
            % Function capturing directions leaving upright position (return as string)
            axisMoved(pos) = find_Direction_Leaving_Upright(currentPosture(pos,1),currentPosture(pos,3));
            disp("Signal NotUpright Detected in Axis: " + axisMoved(pos))
            disp(string(currentPosture(pos,:)))
            subj.bodyDirectionLeaving(pos) = axisMoved(pos);
            uprightDetect(pos) = false;
            
            

        elseif(distPosture(pos) < uprightCheck && ~uprightDetect(pos))
            disp(skeleton(pos) + " IN @" + string(time(i)) + "sec");
            subj.upright(pos) = true;
            disp("Signal Returned-to-Upright Detected")
            disp(string(currentPosture(pos,:)))
            subj.bodyDirectionLeaving(pos) = "";
            uprightDetect(pos) = true;
            axisMoved(pos) = "";
            
            if(uprightDetect(1) && uprightDetect(2) && uprightDetect(3))
                uprightDetect(4) = true;
                disp("=============================")
                disp("STATUS: Torso Back To UPRIGHT ==> " + string(time(i)) + "sec")
                disp("Time Duration: " + string(time(i) - timeNotUpright) + "sec");
                disp("=============================")
                durationUpright = time(i) - timeNotUpright;
                subj.upright(4) = true;
                addTime(subj,durationUpright,1)
                notUprightDetect = "";
                disp(' ')
                disp(' ');
                disp(' ');
                disp(' ');
                disp(' ');
            end
        end 
    end

    
end




% ENDGAME SUMMARY
disp(' ');
disp(' ');
disp(' ');
disp(' ');
disp(' ');
disp(' ');
disp(" ====================================================================")
disp("                       END STATS SUMMARY")
disp(" ====================================================================")


subj
disp(subj.notUprightTime)
disp(subj.notStraightTime_Front)
disp(subj.notStraightTime_Side)
disp(subj.slouchTime)
disp(subj.twistTime_Left)
disp(subj.twistTime_Right)

