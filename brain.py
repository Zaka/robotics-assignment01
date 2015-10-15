# robot goes forward and then slows to a stop when it detects something  
   
from pyrobot.brain import Brain  
   
# class Avoid(Brain):  
           
#    # Give the front two sensors, decide the next move  
#    def determineMove(self, front, left, right):  
#       if front < 0.5:   
#          #print "obstacle ahead, hard turn"  
#          return(0, .3)  
#       elif left < 0.8:
#          #print "object detected on left, slow turn"
#          return(0.1, -.3)  
#       elif right < 0.8: 
#          #print "object detected on right, slow turn" 
#          return(0.1, .3)  
#       else:  
#          #print "clear"  
#          return(0.5, 0.0) 
      
#    def step(self):  
#       front = min([s.distance() for s in self.robot.range["front"]])
#       left = min([s.distance() for s in self.robot.range["left-front"]])
#       right = min([s.distance() for s in self.robot.range["right-front"]])
#       translation, rotate = self.determineMove(front, left, right)  
#       self.robot.move(translation, rotate)

# def INIT(engine):  
#    assert (engine.robot.requires("range-sensor") and
#            engine.robot.requires("continuous-movement"))
#    return Avoid('Avoid', engine)  

class Controller(Brain):  
           
   # Give the front two sensors, decide the next move  
   def determineMove(self, sonar0, sonar2):
      if sonar2 < 0.4:
         # Turn right
         return(0, -.3)
      elif sonar0 < 0.29:
         #print "object detected on sonar0, slow turn"
         return(0.1, -.3)  
      elif sonar0 >= 0.29 and sonar0 <= 0.35: 
         #print "object detected on right, slow turn" 
         return(0.4, 0)  
      else:  
         #print "clear"  
         return(0.1, 0.3) 
      
   def step(self):  
      sonar0 = self.robot.sonar[0][0].value
      sonar2 = self.robot.sonar[0][2].value
      
      translation, rotate = self.determineMove(sonar0, sonar2)  
      self.robot.move(translation, rotate)

def INIT(engine):  
   assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
   return Controller('Controller', engine)  

