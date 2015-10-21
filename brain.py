import datetime
from pyrobot.brain import Brain  
import math

# TODO: Explore the possibility of a smooth turn left

class Controller(Brain):  

   expectedDistance = 0.4              # Expected distance from wall
   h = datetime.datetime.now()         # Elapsed time between loop cycle
   prevDistance = expectedDistance
   tMinusOne = datetime.datetime.now() # Previous time

   HALF_PI = math.pi/2
   
   # This angles are derived from sonar sensors 0, 1 and 2. They are
   # the angles between 0 and 1 ray (alpha) and 1 and 2 (beta).
   BETA = HALF_PI - math.radians(65)
   ALPHA = HALF_PI - math.radians(40)
   
   # Precompute some constants to speed up the algorithm   
   SIN_BETA = math.sin(BETA)
   COS_BETA = math.cos(BETA)
   SIN_ALPHA = math.sin(ALPHA)
   COS_ALPHA = math.cos(ALPHA)
   
   def getReferenceAngle(self, lengthSonar0, lengthSonar1,
                         lengthSonar2):

      if lengthSonar2 <= lengthSonar1:
         sigmaAngle = \
         math.atan((lengthSonar2*self.SIN_ALPHA)/(lengthSonar1 - \
                                             lengthSonar2*self.COS_ALPHA))
      else:
         sigmaAngle = math.atan((lengthSonar2 - \
                                 lengthSonar1*self.COS_ALPHA)/(lengthSonar1*self.SIN_ALPHA)) \
         + math.pi/2 - self.ALPHA

      rotation = self.HALF_PI + self.BETA - sigmaAngle

      return -rotation

   def determineRotation():
      # kP = 5            # Proportional K
      # kI = .00001       # Proportional K
      # kD = .00001       # Derivative K
      # Ti = kP/float(kI) # Integral (constant) time (period)
      # Td = kD/float(kP) # Derivative (constant) time (period)
      # iMinusOne = 0     # Previous integral value
      # dMinusOne = 0     # Previous derivative value

      # error = distanceToWall - self.expectedDistance
      
      # # Proportional
      # P = kP * error
      
      # # Integral
      # I = iMinusOne + kI*self.h*error
      # iMinusOne = I
      
      # # Derivative
      # D = Td/(Td + self.h)*dMinusOne \
      #     - kD/(Td + self.h)*(distanceToWall + self.prevDistance)

      # self.prevDistance = distanceToWall
      # dMinusOne = error
      
      # return (P + I + D)
      

   def determineMove(self, lengthSonar0, lengthSonar1,
                     lengthSonar2):
      speed = 0.3
      return (speed, self.determineRotation(lengthSonar0, lengthSonar1, lengthSonar2))
   
   def step(self):
      lengthSonar0 = self.robot.sonar[0][0].distance()
      lengthSonar1 = self.robot.sonar[0][1].distance()
      lengthSonar2 = self.robot.sonar[0][2].distance()

      distance = min(self.robot.sonar[0][0].value,
                     min([s.distance() for s in self.robot.range["front-left"]]))
      
      translation, rotate = self.determineMove(lengthSonar0, lengthSonar1,
                                               lengthSonar2)

      if self.robot.sonar[0][3].distance() > 0.5 \
         and self.robot.sonar[0][4].distance() > 0.5 \
         and self.robot.sonar[0][3].distance() > self.robot.sonar[0][4].distance():
         # Turn right a little
         rotate = rotate - 0.4
         
      self.robot.move(translation, rotate)

def INIT(engine):  
   assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
   return Controller('Controller', engine)  

