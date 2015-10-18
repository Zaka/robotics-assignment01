# robot goes forward and then slows to a stop when it detects something  

import datetime
from pyrobot.brain import Brain  
   
class Controller(Brain):  

   expectedDistance = 0.4              # Expected distance from wall
   h = datetime.datetime.now() # Elapsed time between loop cycle
   # h = 1                               # Elapsed time between loop cycle
   kP = 5                              # Proportional K
   kI = .00001                        # Proportional K
   kD = .00001                        # Derivative K
   Ti = kP/float(kI)
   Td = kD/float(kP)

   prevDistance = expectedDistance
   tMinusOne = datetime.datetime.now() # Previous time
   iMinusOne = 0                       # Previous integral value
   dMinusOne = 0                       # Previous derivative value

   def determineRotation(self, distanceToWall):
      error = distanceToWall - self.expectedDistance
      
      now = datetime.datetime.now()
      self.h = (now - self.tMinusOne).total_seconds()
      self.tMinusOne = now
      
      # Proportional
      P = self.kP * error
      
      # Integral
      I = self.iMinusOne + self.kI*self.h*error
      self.iMinusOne = I
      
      # Derivative
      D = self.Td/(self.Td + self.h)*self.dMinusOne \
          - self.kD/(self.Td + self.h)*(distanceToWall + self.prevDistance)

      self.prevDistance = distanceToWall
      self.dMinusOne = error
      
      return (P + I + D)
   
   def determineMove(self, distance, frontAll):
      if frontAll < 0.3:
         speed = 0
      else:
         speed = 0.4

      return (speed, self.determineRotation(distance))
   
   def step(self):  
      distance = min([s.distance() for s in self.robot.range["front-left"]])
      frontAll = min([s.distance() for s in self.robot.range["front-all"]])
      
      translation, rotate = self.determineMove(distance, frontAll)  
      self.robot.move(translation, rotate)

def INIT(engine):  
   assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
   return Controller('Controller', engine)  

