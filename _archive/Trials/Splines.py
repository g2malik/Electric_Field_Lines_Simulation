import numpy as np
from scipy import constants
from scipy import *
import tkinter as tk
import copy

##############################################      SETTINGS    #######################################################################

h = 750
w = 1000
p_radius = 7
no_field_lines = 16
field_line_r = 0.75
line_length = 5
line_scale = 2

##############################################      GUI SETUP   #######################################################################
resolution = str(w) + "x" + str(h)

root = tk.Tk()
root.title("Field_Lines")
root.geometry(resolution)

canvas = tk.Canvas(root, height=h, width=w, bg="white")
canvas.grid(column=0, row=0,)

canvas.create_line(0,h/2,w,h/2,dash=4, width=0.1) #x-axis
canvas.create_line(w/2,0,w/2,h,dash=4, width=0.1) # y-axis

def covert_x (coordinate):
    return 10*coordinate+w/2
    
def covert_y (coordinate):
    return 10*coordinate+h/2


def canvas_circle(x,y,r):
    screen_x = 10*x+(w/2)
    screen_y = 10*y+(h/2)
    TL_x = screen_x - r
    TL_y = screen_y + r
    BR_x = screen_x + r
    BR_y = screen_y - r
    return np.array([TL_x, TL_y, BR_x, BR_y])

###########################################        Main Function     #################################################################

#constants
K = 1/(4*np.pi*constants.epsilon_0)
 
def ScaleVector(FieldVector):
    return line_scale*FieldVector/(FieldVector[0]**2 + FieldVector[1]**2)**0.5


def LineStartPoint (x,y,i):
    dtheta = 2*np.pi/no_field_lines
    theta = dtheta * i
    start_x = x + (field_line_r * np.cos(theta))
    start_y = y + (field_line_r * np.sin(theta))
    return [start_x, start_y]
 
class PointCharge:
    def __init__(self, x, y, q):
        self.x = x
        self.y = y
        self.q = q
    
    def FieldVector(self, coordinate):
        direction = np.array([(coordinate[0]-self.x),(coordinate[1]-self.y)])
        unit_vector = direction/(direction[0]**2 + direction[1]**2)**0.5
        magnitude = K*self.q/(direction[0]**2 + direction[1]**2)**0.5
        return unit_vector*magnitude

Points = []

Points.append(PointCharge(10,10,5))
Points.append(PointCharge(-10,-10,5))
Points.append(PointCharge(-10,10,-5))
Points.append(PointCharge(10,-10,-5))

for q in Points:
     param = canvas_circle(q.x,q.y,p_radius)
     
     if q.q>0:
         canvas.create_oval(param[0],param[1], param[2], param[3], fill='red')
     elif q.q<0:
         canvas.create_oval(param[0],param[1], param[2], param[3], fill='blue')
     

for q2 in Points:
    line = 0
    while line < no_field_lines:
        
        OldFieldPoint = np.array([LineStartPoint(q2.x,q2.y,line)[0],LineStartPoint(q2.x,q2.y,line)[1]])
        #print(OldFieldPoint)
        NewFieldPoint = np.array([0,0])
        i = 0
        LinePoints = [OldFieldPoint[0],OldFieldPoint[1]]
        while i < line_length:
            
            TotalField = np.zeros(2)
            
            for q in Points:
                TotalField = TotalField + q.FieldVector(OldFieldPoint)
            
            LineDirection = ScaleVector(TotalField)
            
            if q2.q>0:
                NewFieldPoint = OldFieldPoint + LineDirection
            elif q2.q<0:
                NewFieldPoint = OldFieldPoint - LineDirection
            
            LinePoints.append(NewFieldPoint[0])
            LinePoints.append(NewFieldPoint[1])
            #print(LinePoints)
            
            
            OldFieldPoint = copy.deepcopy(NewFieldPoint)
            i = i+1
        canvas.create_line(covert_x(LinePoints[0]), covert_y(LinePoints[1]),covert_x(LinePoints[2]), covert_y(LinePoints[3]),covert_x(LinePoints[4]), covert_y(LinePoints[5]),covert_x(LinePoints[6]), covert_y(LinePoints[7]),covert_x(LinePoints[8]), covert_y(LinePoints[9]),covert_x(LinePoints[10]), covert_y(LinePoints[11]), fill = "grey", width =1, smooth="true", splinesteps = 8)
        line = line+1
        
root.mainloop()

        


        