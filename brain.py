# robot goes forward and then slows to a stop when it detects something  

import datetime
from pyrobot.brain import Brain  
   
class Controller(Brain):  

   setValue = 0.4                      # Expected distance from wall
   h = 0                               # Elapsed time between loop cycle
   I = 0                               # Integrate value
   P = 0                               # Proportional value
   kP = 1                              # Proportional K
   kI = 1                              # Proportional I
   tMinusOne = datetime.datetime.now() # Previous time
   iMinusOne = 0                       # Previous integrate value
   
   def determineMove(self, frontLeftAndZero, frontAll):
      "First approach, only proportional correction"

      if frontAll < 0.2:
         speed = 0
      else:
         speed = 0.3
         
      error = frontLeftAndZero - self.setValue

      print "frontLeftAndZero:", frontLeftAndZero
      print "speed:", speed
      
      self.h = (datetime.datetime.now() - self.tMinusOne).total_seconds()
      self.tMinusOne = datetime.datetime.now()
      
      # Proportional
      self.P = self.kP*error

      self.I = self.iMinusOne + self.kI*self.h*error
      
      rotation = self.P + self.I
      
      return (speed, rotation)
   
   def step(self):  
      frontLeftAndZero = min(self.robot.sonar[0][0].value,
                 min([s.distance() for s in self.robot.range["front-left"]]))
      frontAll = min([s.distance() for s in self.robot.range["front-all"]])
      
      translation, rotate = self.determineMove(frontLeftAndZero, frontAll)  
      self.robot.move(translation, rotate)

def INIT(engine):  
   assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
   return Controller('Controller', engine)  

