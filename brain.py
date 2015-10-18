import datetime
from pyrobot.brain import Brain  

# TODO: Explore the possibility of a smooth turn left

class Controller(Brain):  

   expectedDistance = 0.4              # Expected distance from wall
   h = datetime.datetime.now()         # Elapsed time between loop cycle
   prevDistance = expectedDistance
   tMinusOne = datetime.datetime.now() # Previous time
   
   def determineRotation(self, distanceToWall):
      kP = 5            # Proportional K
      kI = .00001       # Proportional K
      kD = .00001       # Derivative K
      Ti = kP/float(kI) # Integral (constant) time (period)
      Td = kD/float(kP) # Derivative (constant) time (period)
      iMinusOne = 0     # Previous integral value
      dMinusOne = 0     # Previous derivative value

      error = distanceToWall - self.expectedDistance
      
      # Proportional
      P = kP * error
      
      # Integral
      I = iMinusOne + kI*self.h*error
      iMinusOne = I
      
      # Derivative
      D = Td/(Td + self.h)*dMinusOne \
          - kD/(Td + self.h)*(distanceToWall + self.prevDistance)

      self.prevDistance = distanceToWall
      dMinusOne = error
      
      return (P + I + D)

   def determineMove(self, distance, frontAll):
      now = datetime.datetime.now()
      self.h = (now - self.tMinusOne).total_seconds()
      self.tMinusOne = now

      if frontAll < 0.3:
         speed = 0
      else:
         speed = 0.4

      return (speed, self.determineRotation(distance))
   
   def step(self):  
      distance = min([s.distance() for s in self.robot.range["front-left"]])
      frontAll = min([s.distance() for s in self.robot.range["front-all"]])

      translation, rotate = self.determineMove(distance, frontAll)

      if self.robot.sonar[0][3].distance() > self.robot.sonar[0][4].distance():
         # Turn right a little
         rotate = rotate - 0.4
         
      self.robot.move(translation, rotate)

def INIT(engine):  
   assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
   return Controller('Controller', engine)  

