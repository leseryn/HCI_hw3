import math


size =200

def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx * dx + dy * dy)

def pathlength(A):
    d = 0.0
    for i in range(1,len(A)):
        d = d+distance(A[i-1],A[i])
    return d

def resample(points):
    I= pathlength(points)/ 31
    D = 0.0
    newpoints = [points[0]]
    
    for i in range(1, len(points)):
        d = distance(points[i-1],points[i])
        if (D+d)>=I:
            if d==0:
                d=0.0000001
            qx = points[i-1][0]+((I-D)/d)*(points[i][0]-points[i-1][0])
            qy = points[i-1][1]+((I-D)/d)*(points[i][1]-points[i-1][1])
            q = (int(qx),int(qy))
            newpoints.append(q)
            points[i] = (qx,qy)
            D=0.0
        else: 
            D += d 
    return newpoints

def rotatetozero(points):
    c = centroid(points)
    theta = math.atan2(c[1]-points[0][1],c[0]-points[0][0])
    newpoints = rotateby(points, -theta)
    return newpoints

def centroid(points):
    x=0
    y=0
    for i in range(1,len(points)):
        x += points[i][0]
        y += points[i][1]
    x /= len(points)
    y /= len(points)
    return (int(x),int(y))

def rotateby(points, theta):
    c = centroid(points)
    cos = math.cos(theta)
    sin = math.sin(theta)
    newpoints=[]
    for i in range(0, len(points)-1):
        qx = (points[i][0]-c[0])*cos-(points[i][1]-c[1])*sin+c[0]
        qy = (points[i][0]-c[0])*sin+(points[i][1]-c[1])*cos+c[1]
        q=(int(qx),int(qy))
        newpoints.append(q)
    return newpoints

def scaletosquare(points, size):
    newpoints=[]
    B = boundingbox(points)
    b2=B[2]
    b3=B[3]
    for i  in range(0,len(points)-1):
        if b2==0:  
            b2=0.000000001
        if b3==0:
            b3=0.000000001
        qx = points[i][0]*(size/b2)
        qy = points[i][1]*(size/b3)
        q= (int(qx),int(qy))
        newpoints.append(q)
    return newpoints

def translatetoorigin(points):
    newpoints=[]
    c = centroid(points)
    for i in range(0,len(points)-1):
        qx = points[i][0]-c[0]
        qy = points[i][1]-c[1]
        q = (qx,qy)
        newpoints.append(q)
    return newpoints

def boundingbox(points):
    minX = float("+Inf")
    maxX = float("-Inf")
    minY = float("+Inf")
    maxY = float("-Inf")
    for i in range(0,len(points)-1):
        if points[i][0]<minX:
            minX = points[i][0]
        if points[i][0] > maxX:
            maxX = points[i][0]
        if points[i][1] < minY:
            minY = points[i][1]
        if points[i][1] > maxY:
            maxY = points[i][1]
    return (minX,minY,maxX-minX,maxY-minY)

def distanceatbestangle(points, data, thetaa,thetab,thetad):
    u = 1/2*(-1+math.sqrt(5))
    x1 = u*thetaa + (1-u)*thetab
    f1 = distanceatangle(points, data, x1)
    x2 = (1-u)*thetaa + u*thetab
    f2 = distanceatangle(points, data, x2)
    while abs(thetab-thetaa)>thetad:
        if f1<f2:
            thetab = x2
            x2=x1
            f2=f1
            x1=u*thetaa+(1-u)*thetab
            f1=distanceatangle(points,data,x1)
        else:
            thetaa=x1
            x1=x2
            f1=f2
            x2=(1-u)*thetaa+u*thetab
            f2=distanceatangle(points, data,x2)
    return min(f1,f2)
def distanceatangle(points,data,theta):
    newpoints = rotateby(points, theta)
    d= pathdistance(newpoints, data)
    return d
def pathdistance(A,B):
    d=0.0
    lenA = len(A)
    for i in range(0, lenA-1):
        d=d+distance(A[i],B[i])
    return d/lenA

def transform(points):
    points = resample(points)
    points = rotatetozero(points)
    points = scaletosquare(points,size)
    points = translatetoorigin(points)
    return points


def recognize(points, numcheck):
    b =float("+inf")
    bdata=[]
    bnumber="0"
    score=0.0
    points=transform(points)
    for number in numcheck:
        for data in numcheck[number]:            
            d = distanceatbestangle(points,data,0.79,-0.79,0.03)
            if d<b:
                b=d
                bdata=data
                bnumber=number
    score=1-b/(0.5*math.sqrt(size**2+size**2))
    return(bnumber,score)


position0=[(-103, 18), (-97, 36), (-87, 57), (-77, 77), (-63, 92), (-48, 104), (-32, 109), (-14, 111), (3, 109), (19, 102), (35, 92), (50, 81), (66, 69), (79, 54), (90, 34), (96, 12), (97, -13), (92, -37), (84, -59), (72, -75), (55, -81), (38, -86), (21, -87), (4, -89), (-14, -86), (-30, -82), (-47, -73), (-62, -64)]
position1=[(-96, 88), (-89, 100), (-82, 107), (-75, 111), (-68, 111), (-61, 111), (-54, 111), (-47, 104), (-39, 96), (-32, 85), (-25, 77), (-17, 70), (-11, 73), (-3, 66), (4, 55), (11, 43), (18, 32), (25, 24), (32, 13), (40, 2), (47, -6), (54, -17), (61, -29), (68, -36), (75, -47), (83, -59), (90, -70), (96, -78)]
position2=[(-52, 14), (-64, 4), (-77, -7), (-84, -22), (-84, -38), (-76, -54), (-67, -67), (-57, -81), (-44, -89), (-29, -85), (-16, -76), (-6, -63), (2, -49), (9, -34), (15, -17), (22, -2), (28, 13), (34, 29), (39, 46), (44, 61), (50, 77), (56, 93), (60, 108), (69, 111), (78, 98), (87, 84), (97, 70), (107, 57)]
position3=[(-78, 23), (-85, 5), (-86, -16), (-82, -36), (-75, -56), (-65, -73), (-52, -80), (-37, -71), (-24, -60), (-11, -46), (-5, -25), (-5, -4), (-8, 18), (-11, 38), (-13, 59), (-11, 53), (-2, 36), (9, 20), (23, 8), (37, -3), (52, -10), (67, -1), (79, 13), (92, 26), (102, 43), (110, 62), (114, 82), (112, 103)]
position4=[(-121, 20), (-111, 24), (-100, 31), (-89, 34), (-78, 37), (-68, 39), (-57, 42), (-46, 45), (-35, 46), (-24, 49), (-13, 52), (-2, 54), (9, 57), (20, 60), (31, 64), (42, 67), (53, 70), (60, 63), (61, 45), (62, 27), (64, 10), (66, -8), (67, -26), (72, -42), (73, -60), (75, -78), (77, -96), (78, -112)]
position5=[(-90, 22), (-85, 38), (-79, 54), (-71, 69), (-65, 83), (-56, 97), (-47, 108), (-34, 103), (-22, 96), (-10, 87), (2, 77), (13, 68), (26, 58), (28, 48), (20, 32), (16, 16), (12, -1), (9, -18), (10, -34), (13, -51), (21, -66), (32, -77), (43, -85), (55, -92), (69, -91), (83, -88), (95, -80), (102, -66)]
position6=[(-108, 24), (-110, 45), (-101, 64), (-88, 79), (-72, 89), (-54, 96), (-36, 98), (-17, 96), (0, 88), (17, 77), (34, 69), (50, 58), (65, 45), (78, 29), (87, 10), (90, -11), (90, -33), (85, -53), (77, -73), (66, -91), (51, -101), (33, -102), (15, -94), (0, -81), (-7, -61), (-13, -41), (-11, -19), (-5, 1)]
position7=[(-92, 20), (-88, 9), (-81, -2), (-73, -13), (-66, -24), (-59, -35), (-53, -47), (-47, -59), (-39, -69), (-33, -79), (-25, -69), (-18, -58), (-10, -48), (-3, -37), (5, -26), (12, -16), (20, -5), (27, 6), (34, 16), (42, 26), (49, 37), (57, 48), (64, 58), (71, 69), (79, 80), (86, 90), (94, 100), (101, 111)]
position8=[(-96, 22), (-104, 43), (-99, 68), (-82, 82), (-63, 93), (-42, 98), (-21, 98), (-7, 86), (-4, 59), (-4, 33), (-3, 8), (-3, -17), (0, -42), (6, -67), (18, -88), (36, -102), (56, -100), (74, -89), (86, -66), (96, -44), (95, -19), (91, 6), (79, 24), (60, 36), (39, 33), (20, 23), (0, 18), (-21, 18)]
position9=[(-61, 7), (-72, 24), (-71, 42), (-64, 60), (-47, 73), (-23, 79), (2, 81), (27, 81), (52, 79), (74, 70), (88, 57), (73, 42), (54, 29), (31, 21), (8, 12), (-18, 12), (-41, 12), (-67, 15), (-62, 5), (-42, -7), (-23, -20), (-6, -33), (14, -45), (33, -56), (53, -69), (72, -81), (91, -94), (110, -105)]


numcheck=dict()
numcheck['zero']=[position0]
numcheck['one']=[position1]
numcheck['two']=[position2]
numcheck['three']=[position3]
numcheck['four']=[position4]
numcheck['five']=[position5]
numcheck['six']=[position6]
numcheck['seven']=[position7]
numcheck['eight']=[position8]
numcheck['nine']=[position9]
