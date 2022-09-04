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
root = "C:\Users\tueng\Documents\Tufts Research\";
folder = "\Data_PilotStudy June11\";
folder2 = "\Data_PilotStudy June20";
addpath(root + folder2)

t1 = readtable('Angles_Chest.csv');
totalLength = height(t1); %height(t1)
sample1 = head(t1, totalLength);
Angle_Data1 = table2array(sample1(:,1:4));

%{
t2 = readtable('Angles_Hip.csv');
sample2 = head(t2, totalLength);
Angle_Data2 = table2array(sample2(:,1:4));
az2 = Angle_Data2(:,4);
ay2 = Angle_Data2(:,3);
ax2 = Angle_Data2(:,2);
%}

time = Angle_Data1(:,1);
az1 = Angle_Data1(:,4);
ay1 = Angle_Data1(:,3);
ax1 = Angle_Data1(:,2);


bound = 20;







% ========================================================================
                        % GRAPH ANGLE OF CHEST
% ========================================================================
%subplot(2,1,1)
%curve = animatedline('LineWidth',5,'Color','b');
curve1 = animatedline('LineWidth',2,'Color','r');
curve2 = animatedline('LineWidth',2,'Color','b');
curve3 = animatedline('LineWidth',2,'Color','g');


set(gca, 'XLim',[time(1),time(totalLength)],'YLim',[-bound, bound]);
title("Angles Chest Data")
legend('front+/back- tilt','left-/right+ tilt','left+/right- rotation')
grid on

status = [false, false, false];
numBend = 0;
index = ["front/back","lateral tilt","rotation tilt"];
limitChest = 15;
limitHip = 8;

start = 1;             
step = 10;              
stop = totalLength;


for i=start:step:stop
    addpoints(curve1,time(i),ax1(i));
    addpoints(curve2,time(i),ay1(i));
    addpoints(curve3,time(i),az1(i));
    drawnow;
    
    currentVector = [ax1(i),ay1(i),az1(i)];
    currentVectorAbs = abs(currentVector);
    
    for pos = 1:3
        if(currentVectorAbs(pos) > limitChest && ~status(pos))
            status(pos) = true;
            numBend = numBend + 1;
            disp("BENDING " + string(index(pos)) + " = @" + string(time(i)) + "s");
            disp(string(currentVector(1)) + ',' + string(currentVector(2)) + ',' + string(currentVector(3)));
            disp(' ')
            
        elseif(currentVectorAbs(pos) <= limitChest && status(pos))
            disp("STOPPED " + string(index(pos)) + " = @" + string(time(i)) + "s");
            %disp(i)
            disp(' ')
            status(pos) = false;
        end
    end
end



disp(" ")
disp(" ")
disp(" ============== ")
disp(" ")
disp(" ")



%{
% ========================================================================
                        % GRAPH ANGLE OF HIP
% ========================================================================
subplot(2,1,2)
%curve = animatedline('LineWidth',5,'Color','b');
curve4 = animatedline('LineWidth',2,'Color','r');
curve5 = animatedline('LineWidth',2,'Color','b');
curve6 = animatedline('LineWidth',2,'Color','g');

set(gca, 'XLim',[time(1),time(totalLength)],'YLim',[-bound, bound]);
title("Angles Hip Data")
legend('front+/back- tilt','left-/right+ tilt','left+/right- rotation')
grid on

for i=start:step:stop
    addpoints(curve4,time(i),ax2(i));
    addpoints(curve5,time(i),ay2(i));
    addpoints(curve6,time(i),az2(i));
    drawnow;
    
    currentVector = [ax2(i),ay2(i),az2(i)];
    currentVectorAbs = abs(currentVector);
    
    for pos = 1:3
        if(currentVectorAbs(pos) > limitHip && ~status(pos))
            status(pos) = true;
            numBend = numBend + 1;
            disp("BENDING " + string(index(pos)) + " = @" + string(time(i)) + "s");
            disp(string(currentVector(1)) + ',' + string(currentVector(2)) + ',' + string(currentVector(3)));
            disp(' ')
            
        elseif(currentVectorAbs(pos) <= limitHip && status(pos))
            disp("STOPPED " + string(index(pos)) + " = @" + string(time(i)) + "s");
            %disp(i)
            disp(' ')
            status(pos) = false;
        end
    end
end
%}
