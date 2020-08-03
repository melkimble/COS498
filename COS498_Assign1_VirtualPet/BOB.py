#################################################################
# BOB - An agent that won't tell you what it wants.
# Date: 02/05/2018
#################################################################

import random
import math
class BOB:
    #################################################################
    # Initialize the new object
    # Inputs:
    #  TheCanvas - the canvas widget that BOB will appear in
    #  CenterX - horizontal position of the object in the canvas
    #  CenterY - vertical position of the object in the canvas
    #  FillColor - the color of the BOB
    #  MoodVal - Numeric mood
    #  MoodCode - Bob's mood; Happy, Energetic, Mad/Sad, Angry
     #################################################################
    def __init__(self, TheCanvas, CenterX,CenterY,Type,FillColor, MoodVal):
	# Save the values that are passed in so we can access them in the Update() function
	self.TheCanvas = TheCanvas 

	self.CenterX=CenterX
	self.CenterY=CenterY
	
	self.Type=Type
	self.FillColor=FillColor
	
	self.MoodVal=MoodVal
	
	# create Bob's face at the specifed x and y location 
	self.id = self.TheCanvas.create_rectangle(CenterX-WIDTH/2, CenterY-HEIGHT/2,
            CenterX+WIDTH/2, CenterY+HEIGHT/2,fill=FillColor) 
	
	#################################################################
	# Update the state of the individual
	# This includes:
	# - MoodVal
	#################################################################	
	def Update(self,TheMood): 
	    # update the counters/mood	    
	    self.MoodVal=MoodVal-1
	    
	    # check for mood
	    