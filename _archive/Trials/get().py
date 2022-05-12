import numpy as np
from scipy import constants
import tkinter as tk
import copy

##############################################      SETTINGS    #######################################################################
window_w = 1200
h = 750
w = 800
graph_scale = 10
p_radius = 7
field_lines_C = 3
field_line_r = p_radius/graph_scale + 0.5
line_length = 2000
line_scale = 0.1

bag = "#8bab74"
frame_width = 0
##############################################      SETUP   #######################################################################
charge_points = []
row_n = 1
##############################################      GUI   #######################################################################

def add_charge():
    x=int(x_ent.get())
    y=-int(y_ent.get())
    q=int(q_ent.get())
    canvas.delete("all")
    canvas.create_line(0,h/2,w,h/2,dash=4, width=0.1) #x-axis
    canvas.create_line(w/2,0,w/2,h,dash=4, width=0.1) # y-axis
    MainFunc(x,y,q)
    
    global row_n
    
    q2_lab = tk.Label(b3_frame, text=q, bg= bag)
    x2_lab = tk.Label(b3_frame, text=x, bg= bag)
    y2_lab = tk.Label(b3_frame, text=y, bg= bag)
    q2_lab.grid(column = 0,row = row_n, padx =[15,0])
    x2_lab.grid(column = 1,row = row_n, padx =[25,0])
    y2_lab.grid(column = 2,row = row_n, padx =[25,0])
    
    row_n = row_n+1
    

resolution = str(window_w) + "x" + str(h)

root = tk.Tk()
root.title("Electric Field Visualization")
root.geometry(resolution)
root['bg'] = bag

c_frame = tk.LabelFrame(root)
c_frame.grid(column = 0, row =0)
c_frame['borderwidth'] = frame_width

b_frame = tk.LabelFrame(root)
b_frame.grid(column = 1, row = 0, sticky = "n", padx=30)
b_frame['borderwidth'] = frame_width
b_frame['bg'] = bag

b2_frame = tk.LabelFrame(b_frame)
b2_frame.grid(column = 0, row = 1, sticky = "n", pady=20)
b2_frame['borderwidth'] = frame_width
b2_frame['bg'] = bag

h1_frame = tk.LabelFrame(b_frame)
h1_frame.grid(column = 0, row = 0, sticky = "n")
h1_frame['borderwidth'] = frame_width
h1_frame['bg'] = bag

h2_frame = tk.LabelFrame(b_frame)
h2_frame.grid(column = 0, row = 2, sticky = "n")
h2_frame['borderwidth'] = frame_width
h2_frame['bg'] = bag


b3_frame = tk.LabelFrame(b_frame)
b3_frame.grid(column = 0, row = 3, sticky = "n", pady=10)
b3_frame['borderwidth'] = frame_width
b3_frame['bg'] = bag

canvas = tk.Canvas(c_frame, height=h, width=w, bg="white")
canvas.grid(column=0, row=0,padx= [20,0])

canvas.create_line(0,h/2,w,h/2,dash=4, width=0.1) #x-axis
canvas.create_line(w/2,0,w/2,h,dash=4, width=0.1) # y-axis

H1 = tk.Label(h1_frame, text = "--------------------- New Charge ---------------------",bg= bag)
H1.grid(column=0, row=0)

H2 = tk.Label(h2_frame, text = "------------------- Charges Present ------------------",bg= bag)
H2.grid(column=0, row=0)

q_lab = tk.Label(b2_frame, text = "Charge",bg= bag)
x_lab = tk.Label(b2_frame, text = "x-coordinate",bg= bag)
y_lab = tk.Label(b2_frame, text = "y-coordinate",bg= bag)
q_lab.grid(column = 0,row = 0, padx =[15,0])
x_lab.grid(column = 1,row = 0, padx =[15,0])
y_lab.grid(column = 2,row = 0, padx =[15,0])

q2_lab = tk.Label(b3_frame, text = "Charge",bg= bag)
x2_lab = tk.Label(b3_frame, text = "x-coordinate",bg= bag)
y2_lab = tk.Label(b3_frame, text = "y-coordinate",bg= bag)
q2_lab.grid(column = 0,row = 0, padx =[15,0])
x2_lab.grid(column = 1,row = 0, padx =[25,0])
y2_lab.grid(column = 2,row = 0, padx =[25,0])


q_ent = tk.Entry(b2_frame, width = "10", bd="0")
x_ent = tk.Entry(b2_frame, width = "10", bd= "0")
y_ent = tk.Entry(b2_frame, width = "10", bd="0")

q_ent.grid(column = 0,row = 1, padx =[15,0])
x_ent.grid(column = 1,row = 1, padx = [15,0])
y_ent.grid(column = 2,row = 1, padx = [15,0])

add_button = tk.Button(b2_frame, text = "Add New Charge", command=add_charge)
add_button.grid(column=1, row=2, padx=[15,0], pady=[15,0])

def acovert_x (coordinate):
    return  graph_scale*coordinate[0]+w/2
    
def acovert_y (coordinate):
    return graph_scale*coordinate[1]+h/2

def canvas_circle(x,y,r):
    screen_x = graph_scale*x+(w/2)
    screen_y = graph_scale*y+(h/2)
    TL_x = screen_x - r
    TL_y = screen_y + r
    BR_x = screen_x + r
    BR_y = screen_y - r
    return np.array([TL_x, TL_y, BR_x, BR_y])

###########################################        Main Function     #################################################################

#constants
K = 1/(4*np.pi*constants.epsilon_0)

skip=0

def ScaleVector(FieldVector):
    return line_scale*FieldVector/(FieldVector[0]**2 + FieldVector[1]**2)**0.5

def LineStartPoint (x,y,i, no_field_lines):
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


#charge_points.append(PointCharge(20,0,-5))
#charge_points.append(PointCharge(-20,0,5))
#charge_points.append(PointCharge(0,-20,5))
#charge_points.append(PointCharge(10,-10,-5))

# Delete canvas and start from here once the button is pressed 

def MainFunc(xf,yf,qf):
    charge_points.append(PointCharge(xf,yf,qf))
    
    for q in charge_points:
         param = canvas_circle(q.x,q.y,p_radius)
         
         if q.q>0:
             canvas.create_oval(param[0],param[1], param[2], param[3], fill='red')
         elif q.q<0:
             canvas.create_oval(param[0],param[1], param[2], param[3], fill='blue')
    
    
    for q2 in charge_points:
        line = 0
        no_field_lines = int(abs(q2.q*field_lines_C))
        
        while line < no_field_lines:
            
            OldFieldPoint = np.array([LineStartPoint(q2.x,q2.y,line, no_field_lines)[0],LineStartPoint(q2.x,q2.y,line, no_field_lines)[1]])
            NewFieldPoint = np.array([0,0])
            i = 0
                        
            while i < line_length:
                i = i+1
                
                if abs(OldFieldPoint[0])> ((w/graph_scale/2)) or abs(OldFieldPoint[1])> ((h/graph_scale/2)):
                    break
                
                for q3 in charge_points:
                    if ((q3.x - OldFieldPoint[0])**2 + (q3.y - OldFieldPoint[1])**2)**0.5 < field_line_r - 0.05:
                        global skip
                        skip = 1
                        break
                
                if skip == 1:
                    skip = 0
                    break
                                
                TotalField = np.zeros(2)
                
                for q in charge_points:
                    TotalField = TotalField + q.FieldVector(OldFieldPoint)
                
                LineDirection = ScaleVector(TotalField)
                
                if q2.q>0:
                    NewFieldPoint = OldFieldPoint + LineDirection
                elif q2.q<0:
                    NewFieldPoint = OldFieldPoint - LineDirection
                
                canvas.create_line(acovert_x(OldFieldPoint), acovert_y(OldFieldPoint), acovert_x(NewFieldPoint), acovert_y(NewFieldPoint), fill = "grey", width =1)
                
                OldFieldPoint = copy.deepcopy(NewFieldPoint)
                
            line = line+1

root.mainloop()

        


        