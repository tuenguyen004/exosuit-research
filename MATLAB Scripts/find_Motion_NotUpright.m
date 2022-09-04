function [direction] = find_Motion_NotUpright(frontBack,leftRight)

    xStatus = "";
    zStatus = "";
    direction = "";

    % determining if X and/or Z direction are negative or not
    if(leftRight > 10)        %right = angle(+) & left = angle(-)
        xStatus = "X-";
    elseif(leftRight < -10)
        xStatus = "X";
    end
    if(frontBack > 0)
        zStatus = "Z";
    elseif(frontBack < 0)
        zStatus = "Z-";
    end
    
    
    absLR = abs(leftRight);
    absFB = abs(frontBack);

    % displaying Direction & which is stronger
    if(absFB > 12 && absLR < 12)
        direction = zStatus;
    elseif(absFB < 12 && absLR > 12)
        direction = xStatus;
    elseif(absFB > 12 && absLR > 12)
        if(absLR > absFB)
            direction = xStatus + " " + zStatus;
        elseif(absLR < absFB)
            direction = zStatus + " " + xStatus;
        else
            direction = xStatus + " = " + zStatus;
        end
    end
    
end

