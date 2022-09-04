function [output] = find_Direction_Leaving_Upright(x,z)
    % =====================================================================
    % RETURN A STRING OF WHICH DIRECTION(S) THE OBJECT IS LEAVING UPRIGHT
    % =====================================================================
    
    diff = abs(x) - abs(z);
    motionCheck = 0.02;     % Threshold of x & z position before considered the presence of that
                            %   axis in the object's motion
    diffXZ = 0.03;          % Threshold of x & z position before considered the presence of that
                            %   axis RELATIVE TO EACH OTHER in the object's motion 
    output = "";
                            
    if(abs(x) > motionCheck || abs(z) > motionCheck)
        if(diff > 0 && abs(diff) > diffXZ)
            output = "X";
            if(x < 0)
                output = output + "-";
            end
        elseif(diff < 0 && abs(diff) > diffXZ)
            output = "Z";
            if(z < 0)
                output = output + "-";
            end
        elseif(diff > 0 && abs(diff) <= diffXZ)
            output = "X Z";
            if(x < 0 && z < 0)
                output = "X- Z-";
            elseif(x < 0 && z > 0)
                output = "X- Z";
            elseif(x > 0 && z < 0)
                output = "X Z-";
            end
        elseif(diff < 0 && abs(diff) <= diffXZ)
            output = "Z X";
            if(x < 0 && z < 0)
                output = "Z- X-";
            elseif(x < 0 && z > 0)
                output = "Z X-";
            elseif(x > 0 && z < 0)
                output = "Z- X";
            end
        end
    end
end

