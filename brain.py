# robot goes forward and then slows to a stop when it detects something  

import datetime
from pyrobot.brain import Brain  
   
class Controller(Brain):  

   setValue = 0.4                      # Expected distance from wall
   h = datetime.datetime.now()                               # Elapsed time between loop cycle
   kP = 5                              # Proportional K
   kI = 2                              # Proportional K
   kD = 1.5                              # Derivative K
   tMinusOne = datetime.datetime.now() # Previous time
   iMinusOne = 0                       # Previous integral value
   dMinusOne = 0                       # Previous derivative value
   
   def determineMove(self, frontLeftAndZero, frontAll):

      if frontAll < 0.3:
         speed = 0
      else:
         speed = 0.4

      # speed = 0.3
      
      error = frontLeftAndZero - self.setValue

      now = datetime.datetime.now()
      self.h = (now - self.tMinusOne).total_seconds()
      self.tMinusOne = now
      
      # Proportional
      P = self.kP * error
      # Integral
      I = self.iMinusOne + self.kI*self.h*error
      # print "iMinusOne:", self.iMinusOne
      self.iMinusOne = I
      # Derivative
      D = self.kD * (error - self.dMinusOne)/self.h
      # print "dMinusOne:", self.dMinusOne
      self.dMinusOne = error
      rotation = P + I + D

      # # DEBUG
      # print "Kp:", self.kP
      # print "Ki:", self.kI
      # print "Kd:", self.kD
      # print "h:", self.h
      # print "error:", error
      # print "frontLeftAndZero:", frontLeftAndZero
      # print "speed:", speed
      # print "P:", P
      # print "I:", I
      # print "D:", D
      # print "rotation:", rotation
      # print
      
      return (speed, rotation)
   
   def step(self):  
      # frontLeftAndZero = min(self.robot.sonar[0][0].value,
      #            min([s.distance() for s in self.robot.range["front-left"]]))
      frontAll = min([s.distance() for s in self.robot.range["front-all"]])
      
      translation, rotate = self.determineMove(frontLeftAndZero, frontAll)  
      self.robot.move(translation, rotate)

def INIT(engine):  
   assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
   return Controller('Controller', engine)  

