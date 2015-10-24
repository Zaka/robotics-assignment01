import datetime
from pyrobot.brain import Brain  
import math

class Controller(Brain):  

   expectedDistance = 0.5              # Expected distance from wall
   h = .2         # 200 ms
   prevDistance = expectedDistance
   prevError = 0
   MAX_ANGLE = 1.4
   
   def determineRotation(self, distanceToWall):
      kP = 0.7           # Proportional K
      kI = .5      # Integral K
      kD = .1       # Derivative K
      # kP = .7                     # Proportional K
      # kI = 0.5 # Integral K
      # kD = .5 # Derivative K
      Ti = kP/float(kI)            # Integral (constant) time (period)
      Td = kD/float(kP)            # Derivative (constant) time (period)
      iMinusOne = 0                # Previous integral value
      dMinusOne = 0                # Previous derivative value
      
      error = distanceToWall - self.expectedDistance
      
      # Proportional
      P = kP * error
      
      # Integral
      I = iMinusOne + kI*self.h*error
      iMinusOne = I
      
      # Derivative
      D = (error - self.prevError)/self.h
      self.prevError = error

      rotation = (P + I + D)

      return rotation

   def determineMove(self, distance, frontAll):
      if frontAll < 0.3:
         speed = 0
      else:
         speed = 1

      return (speed, self.determineRotation(distance))
   
   def step(self):  
      distance = min(self.robot.sonar[0][0].distance(),
                     self.robot.sonar[0][1].distance(),
                     self.robot.sonar[0][2].distance(),
                     self.robot.sonar[0][3].distance(),
                     self.robot.sonar[0][15].distance())

      frontAll = min([s.distance() for s in self.robot.range["front-all"]])

      translation, rotate = self.determineMove(distance, frontAll)

      if self.robot.sonar[0][3].distance() < self.expectedDistance \
         and self.robot.sonar[0][4].distance() < self.expectedDistance \
         and self.robot.sonar[0][3].distance() > self.robot.sonar[0][4].distance():
         # Turn right a little
         print "Turning right"
         rotate = rotate - 3
         
      self.robot.move(translation, rotate)

def INIT(engine):  
   assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
   return Controller('Controller', engine)  

