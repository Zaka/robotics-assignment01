"""
Mundo de Zaka
"""

from pyrobot.simulators.pysim import *

def INIT():
    TkWorldWidth = TkWorldHeight = 600
    TkOuterBoxWidth = TkOuterBoxHeight = 550
    TkScale = 80
    TkOffsetX = (TkWorldWidth - TkOuterBoxWidth)/2
    TkOffsetY = TkWorldHeight - (TkWorldHeight - TkOuterBoxHeight)/2

    print "(width, height)", (TkWorldWidth, TkWorldHeight)
    print "(offset x, offset y)", (TkOffsetX, TkOffsetY)
    
    # (width, height), (offset x, offset y), scale:
    # sim = TkSimulator((446,491),(21,451),80.517190)
    sim = TkSimulator((TkWorldWidth,TkWorldHeight),
                      (TkOffsetX, TkOffsetY),
                      TkScale)
    
    # x1, y1, x2, y2 in meters:
    sim.addBox(0, 0, 7, 7)
    # sim.addShape("polygon",
    #              (2,0),(2,4),(1,4),(1,6),(2,6),(2,7),(0.2,7),(0.2,0),
    #              fill = "blue",
    #              outline = "blue")

    sim.addWall(2, 0, 2, 4, color="black")
    sim.addWall(2, 4, 1, 4, color="black")
    sim.addWall(1, 4, 1, 6, color="black")
    sim.addWall(1, 6, 2, 6, color="black")
    sim.addWall(2, 6, 2, 7, color="black")
    sim.addWall(0.2, 7, 0.2, 0, color="black")
    
    # sim.addBox(0, 4, 1, 5, "blue", wallcolor="blue")
    # sim.addBox(2.5, 0, 2.6, 2.5, "green", wallcolor="green")
    # sim.addBox(2.5, 2.5, 3.9, 2.6, "green", wallcolor="green")

    
    # port, name, x, y, th, bounding Xs, bounding Ys, color
    # (optional TK color name):
    # sim.addRobot(60000, TkPioneer("RedPioneer",
    #                               .5, 2.5, 0.00,
    #                               ((.225, .225, -.225, -.225),
    #                                (.175, -.175, -.175, .175))))
    sim.addRobot(60000, TkPioneer("RedPioneer",
                                  2.5, 0.5, 0.00,
                                  ((.225, .225, -.225, -.225),
                                   (.175, -.175, -.175, .175))))

    
    # add some sensors:
    # sim.robots[0].addDevice(PioneerFrontSonars()) # for 8 front sonar
    sim.robots[0].addDevice(Pioneer16Sonars()) # for full 360 sonar
    sim.robots[0].addDevice(PioneerFrontLightSensors())
    # x, y relative to body center (beyond bounding box):
    sim.robots[0].addDevice(BulbDevice(0.226, 0)) # pose x, pose y
    # width, height, startAngle, stopAngle, pose x, pose y, pose thr:
    # cam = Camera(60, 40, 0, 120, 0, 0, 0)
    # sim.robots[0].addDevice(cam)
    # sim.robots[0].addDevice( PTZ(cam) )
    return sim
