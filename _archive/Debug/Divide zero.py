import numpy as np
from scipy import constants
from scipy import *
import tkinter as tk
import copy

##############################################      SETTINGS    #######################################################################

h = 500
w = 500
p_radius = 5
no_field_lines = 8
field_line_r = 1

##############################################      GUI SETUP   #######################################################################
resolution = str(w) + "x" + str(h)

root = tk.Tk()
root.title("Field_Lines")
root.geometry(resolution)

canvas = tk.Canvas(root, height=h, width=w, bg="white")
canvas.grid(column=0, row=0,)

canvas.create_line(0,h/2,w,h/2,) #x-axis
canvas.create_line(w/2,0,w/2,h,) # y-axis

def acovert_x (coordinate):
    return 10*coordinate[0]+w/2
    
def acovert_y (coordinate):
    return 10*coordinate[1]+h/2


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
 
def UnitVector(FieldVector):
        return FieldVector/(FieldVector[0]**2 + FieldVector[1]**2)**0.5

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

Points.append(PointCharge(-10,0,5))
Points.append(PointCharge(10,0,-5))
#Points.append(PointCharge(0,-10,5))
#Points.append(PointCharge(0,10,5))

for q in Points:
     param = canvas_circle(q.x,q.y,p_radius)
     #print(param)
     canvas.create_oval(param[0],param[1], param[2], param[3], fill='black')

for q in Points:
    line = 0
    while line < no_field_lines:
        
        OldFieldPoint = np.array([LineStartPoint(q.x,q.y,line)[0],LineStartPoint(q.x,q.y,line)[1]])
        NewFieldPoint = np.array([0,0])
        i = 0
        while i < 60:
            
            TotalField = np.zeros(2)
            
            for q in Points:
                TotalField = TotalField + q.FieldVector(OldFieldPoint)
            
            LineDirection = UnitVector(TotalField)
            NewFieldPoint = OldFieldPoint - LineDirection
        
            canvas.create_line(acovert_x(OldFieldPoint), acovert_y(OldFieldPoint), acovert_x(NewFieldPoint), acovert_y(NewFieldPoint))
                         
            OldFieldPoint = copy.deepcopy(NewFieldPoint)
            i = i+1
        line = line+1

root.mainloop()

        


        