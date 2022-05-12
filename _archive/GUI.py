import tkinter as tk
import numpy as np

h = 500
w = 500
p_radius = 1
resolution = str(w) + "x" + str(h)

root = tk.Tk()
root.title("Field_Lines")
root.geometry(resolution)

main_canvas = tk.Canvas(root, height=h, width=w, bg="white")
main_canvas.grid(column=0, row=0,)

main_canvas.create_line(0,h/2,w,h/2) #x-axis
main_canvas.create_line(w/2,0,w/2,h) # y-axis

root.mainloop()

def covert_x (coordinate):
    return 5*(coordinate[0]+w/2)
    
def covert_y (coordinate):
    return 5*(coordinate[1]+h/2)
    