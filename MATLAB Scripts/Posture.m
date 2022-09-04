classdef Posture < handle
    
    properties (Access = public)
        upright = [true,true,true,true];
        straight = [true,""];
        slouch = false;
        twist = [false,""];
        
        numNotUpright = 0;              
        numNotStraight = 0;         
        numSlouch = 0;                  
        numTwist = 0;                   
        
        notUprightTime = [];
        notStraightTime_Front = [];
        notStraightTime_Side = []
        slouchTime = [];
        twistTime_Left = [];
        twistTime_Right = [];
        
        bodyDirectionLeaving = ["","",""];
        notUprightDirection = "";
        
        
    end
    
    methods
        %Adding Time Interval of Each Category
        function addTime(obj,timeDuration,id)
            if(id == 1)
                obj.notUprightTime = [obj.notUprightTime,timeDuration];
            elseif(id == 2)
                if(obj.straight(2) == "front")
                    obj.notStraightTime_Front = [obj.notStraightTime_Front,timeDuration];
                elseif(obj.straight(2) == "side")
                    obj.notStraightTime_Side = [obj.notStraightTime_Side,timeDuration];
                end
            elseif(id == 3)
                obj.slouchTime = [obj.slouchTime,timeDuration];
            elseif(id == 4)
                if(obj.twist(2) == "left")
                    obj.twistTime_Left = [obj.twistTime_Left,timeDuration];
                elseif(obj.twist(2) == "right")
                    obj.twistTime_Right = [obj.twistTime_Right,timeDuration];
                end
            else
                disp("ERROR: ID out of bound for " + string(timeDuration))
            end
        end
    end
    
    
    
    
    
end

