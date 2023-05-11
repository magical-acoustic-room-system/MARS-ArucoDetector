from math import sqrt, acos, asin, pi, sin

def position(r1,r2):
    # Input values
    h = 10
    x = 5
    y = 8

    # Calculate distance between A and B
    d = sqrt((x - 0)**2 + (y - 0)**2 + (h - h)**2)

    # Calculate height of C
    cosC = (r1**2 + r2**2 - d**2) / (2 * r1 * r2)
    hC = sqrt(r1**2 - (r2*cosC)**2)

    # Calculate position of C on the xy-plane
    sinA = hC / r1
    sinB = hC / r2
    angleA = asin(sinA)
    angleB = asin(sinB)
    angleC = pi - angleA - angleB
    cx = r1 * sin(angleA)
    cy = r2 * sin(angleB)

    # Output result
    print("Position of C on the floor: ({:.2f}, {:.2f}, {:.2f})".format(cx, cy, 0))
    return cx, cy, 0