from tkinter import *
import math
line_depth=1
top = Tk()
DIMENSION=250
top.rowconfigure(0,weight=1)
top.columnconfigure(0,weight=1)
canvas=Canvas(top,bg="white",height=DIMENSION,width=DIMENSION,)
canvas.grid(row=0,column=0,sticky='nsew')
grid=[]
lines=[]
current=1
x=None
y=None
first=False
line_size=Entry(top,bd=5)
color="black"
side_length=1

def set_line_depth():
    global line_depth
    if line_size.get().isnumeric():
        print(line_depth)
        line_depth=int(line_size.get())

def set_to_brush():
    global current
    current=0
def set_to_line():
    global current
    current=1
def set_to_fill():
    global current
    current=2


def initialize_grid():
    global lines,grid
    for x in range(0,round(DIMENSION/side_length)):
        grid.append([])
        lines.append(canvas.create_line(x*side_length,0,x*side_length,DIMENSION))
        lines.append(canvas.create_line(0,x*side_length,DIMENSION,x*side_length))
        for y in range(0,round(DIMENSION/side_length)):
            grid[x].append("white")
def delete_lines():
    global lines
    for line in lines:
        canvas.delete(line)
def fill_color(current_x,current_y,change):
    global grid,color
    color_current(current_x*side_length,current_y*side_length)
    for change_y in range(-1,2):
        if current_y+change_y>0 and current_y+change_y<DIMENSION:
            for change_x in range(-1,2):
                if not(change_x==0 and change_y==0):
                    if current_x+change_x>0 and current_x+change_x<DIMENSION and grid[current_x+change_x][current_y+change_y]==change:
                        fill_color(current_x+change_x,current_y+change_y,change)
def bucket_command(event):
    if event.x<=DIMENSION and event.y<=DIMENSION and event.x>=0 and event.y>=0:
        global color
        current_color=grid[math.floor(event.x/side_length)][math.floor(event.y/side_length)]
        if current_color != color:
            fill_color(math.floor(event.x/side_length),math.floor(event.y/side_length),current_color)
#def change_grid(new_length):
   #global grid
    #old_tile_size=DIMENSION/side_length
    #new_tile_size=DIMENSION/new_length
    #new_grid=[]
    #for x in range(0,DIMENSION/new_tile_size):
        #new_grid.append([])
        #for y in range(0, DIMENSION / new_tile_size):


def diselect(event):
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonRelease>")
    canvas.bind("<Button-1>",eventhandler)
def show_color(new_color):
    color_op()
    global color
    color=new_color
def color_depth(current_x,current_y):
    global line_depth
    cord_x=math.floor(current_x/side_length)
    cord_y = math.floor(current_y / side_length)
    for change_x in range(cord_x-line_depth,cord_x+line_depth):
        for change_y in range(cord_y-line_depth,cord_y+line_depth):
            if change_x>=0 and change_x<DIMENSION and change_y>=0 and change_y<DIMENSION:
                color_current(change_x,change_y)
def color_current(current_x,current_y):
    if current_x<=DIMENSION and current_y<=DIMENSION:
        global grid
        grid[math.floor(current_x/side_length)][math.floor(current_y/side_length)] = color
        set_x=math.floor(current_x/side_length)*side_length
        set_y=math.floor(current_y/side_length)*side_length
        change_x=side_length
        change_y=side_length
        if set_x+change_x>=DIMENSION:
            change_x-=set_x+change_x-DIMENSION
        if set_y+change_y>=DIMENSION:
            change_y-=set_y+change_y-DIMENSION
        canvas.create_rectangle(set_x, set_y, set_x+change_x, set_y+change_y, fill=color, outline=color)
def addLine(event):
    global x,y,first,side_length
    dif_x = math.floor((event.x-x)/side_length)
    dir_x=0
    if dif_x!=0:
        dir_x=dif_x/abs(dif_x)
    dif_y = math.floor((event.y-y)/side_length)
    dir_y=0
    if dif_y!=0:
        dir_y = dif_y / abs(dif_y)
    if abs(dif_x)>abs(dif_y):
        if dif_y==0:
            for num in range(min(0,dif_x),max(0,dif_x)):
                color_current(x+num*side_length,y)
        else:
            rate=math.floor(abs(dif_x)/abs(dif_y))
            module=0
            if abs(dif_x)%abs(dif_y)!=0:
                module=math.floor(abs(dif_y)/(abs(dif_x)%abs(dif_y)))
            current_x=event.x
            dir_current=dir_x*-1
            if dir_y==1:
                current_x=x
                dir_current=dir_x

            for current_y in range(min(event.y, y), max(event.y, y),side_length):
                if module!=0 and (current_y-min(event.y,y))%module==0:
                    for gradient in range(min(0,rate+1),max(0,rate+1),side_length):
                        color_depth(current_x,current_y)
                        current_x+=side_length*dir_current
                else:
                    for gradient in range(min(0,rate),max(0,rate),side_length):
                        color_depth(current_x, current_y)
                        current_x+=side_length*dir_current
    else:
        if dif_x==0:
            if dif_y==0:
                return None
            for num in range(min(0,dif_y),max(0,dif_y)):
                color_depth(x,y+num*side_length)
        else:
            rate=math.floor(abs(dif_y)/abs(dif_x))
            module = 0
            if abs(dif_y)%abs(dif_x)!=0:
                module = math.floor(abs(dif_x) / abs(dif_y) % abs(dif_x))

            current_y=event.y
            current_dir=dir_y*-1
            if dir_x==1:
                current_y=y
                current_dir=dir_y
            for current_x in range(min(event.x,x),max(event.x,x),side_length):
                if module!=0 and (current_x-min(event.x,x))%module==0:
                    for gradient in range(min(0,rate+1),max(0,rate+1),side_length):
                        color_depth(current_x,current_y)
                        current_y+=current_dir*side_length

                else:
                    for gradient in range(min(0,rate),max(0,rate),side_length):
                        color_depth(current_x, current_y)
                        current_y+=current_dir*side_length

    first=False
def brush(event):
    global x, y
    x=event.x
    y=event.y
    color_depth(x, y)
def click(event):
    global x, y, first

    if first:

        addLine(event)
        first=False
    else:
        x = math.floor(event.x/side_length)*side_length
        y = math.floor(event.y/side_length)*side_length
        first=True

def eventhandler(event):
    global current,x,y

    if current==0:
        canvas.bind("<B1-Motion>", brush)
        canvas.bind("<ButtonRelease>", diselect)
    elif current==1:
        click(event)
        diselect(event)
    elif current==2:
        canvas.bind("<B1-Motion>", bucket_command)
        canvas.bind("<ButtonRelease>", diselect)
def color_op():
    id=canvas.create_rectangle(10,10,30,30,fill='Black')
    canvas.tag_bind(id,"<Button-1>",lambda x:show_color("Black"))
    id= canvas.create_rectangle(10, 40, 30, 60, fill='gray')
    canvas.tag_bind(id, "<Button-1>", lambda x: show_color("gray"))
    id=canvas.create_rectangle(10, 70, 30, 90, fill='brown4')
    canvas.tag_bind(id, "<Button-1>", lambda x: show_color("brown4"))
    id=canvas.create_rectangle(10, 100, 30, 120, fill='red')
    canvas.tag_bind(id, "<Button-1>", lambda x: show_color("red"))
    id=canvas.create_rectangle(10, 130, 30, 150, fill='yellow')
    canvas.tag_bind(id, "<Button-1>", lambda x: show_color("yellow"))
    id=canvas.create_rectangle(10, 160, 30, 180, fill='green')
    canvas.tag_bind(id, "<Button-1>", lambda x: show_color("green"))
    id=canvas.create_rectangle(10, 190, 30, 210, fill='blue')
    canvas.tag_bind(id, "<Button-1>", lambda x: show_color("blue"))
    id=canvas.create_rectangle(10, 220, 30, 240, fill='purple')
    canvas.tag_bind(id, "<Button-1>", lambda x: show_color("purple"))


def main():
    label = Label(top, text="Depth")
    label.grid(column=1,row=0)

    line_size.grid(column=2,row=0)
    submit=Button(top,text="SUBMIT",command=set_line_depth)
    submit.grid(column=1,row=1)
    ToolMenu = Menu(top)
    top.config(menu=ToolMenu)
    submenu=Menu(ToolMenu)
    top.title("paint")
    initialize_grid()
    color_op()
    canvas.bind("<Button-1>", eventhandler)
    ToolMenu.add_command(label="Brush",command=set_to_brush)
    ToolMenu.add_command(label="Line", command=set_to_line)
    ToolMenu.add_command(label="Fill", command=set_to_fill)
    ToolMenu.add_cascade(label="Tool", menu=submenu)
    delete_lines()
    top.mainloop()

main()