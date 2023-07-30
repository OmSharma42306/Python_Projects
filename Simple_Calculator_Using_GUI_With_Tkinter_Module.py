from tkinter import *
root=Tk()
root.title("Om Sharma's Calculator")
entry=Entry(root,border="10",width="50")
entry.grid(row="0",column="0",columnspan="3")


# This Function is Use to take input from GUI Multiple values at a time
def button_click(number):
    current=entry.get()
    entry.delete(0,END)
    entry.insert(0,str(current)+str(number))
    

# This Function is used to Clear the Values
def button_clear():
    entry.delete(0,END)

# Addition Function
def button_add():
    first=entry.get()       # ---> Here Our First entry will be stored in first variable
    global f_num
    global math
    math="Addition"            # ---> Here we are Declaring global variable to store first value
    f_num=int(first)        
    entry.delete(0,END)

# Substraction Function
def button_minus():
    first=entry.get()       # ---> Here Our First entry will be stored in first variable
    global f_num
    global math
    math="Minus"            # ---> Here we are Declaring global variable to store first value
    f_num=int(first)        
    entry.delete(0,END)

# Multiplication Function
def button_multiply():
    first=entry.get()       # ---> Here Our First entry will be stored in first variable
    global f_num
    global math
    math="Multiplication"            # ---> Here we are Declaring global variable to store first value
    f_num=int(first)        
    entry.delete(0,END)

# Division Function
def button_divide():
    first=entry.get()       # ---> Here Our First entry will be stored in first variable
    global f_num
    global math
    math="Division"            # ---> Here we are Declaring global variable to store first value
    f_num=int(first)        
    entry.delete(0,END)
    

# Equal Function
def Equal():
    second=entry.get()
    entry.delete(0,END)
    # Here i created a math variable to identify the Operation so in add function i stored math value Addition so it will Make add Operation
    if math=="Addition":
        entry.insert(0,f_num + int(second))
    elif math=="Minus":
        entry.insert(0,f_num - int(second))
    elif math=="Multiplication":
        entry.insert(0,f_num * int(second))
    elif math=="Division":
        entry.insert(0,f_num / int(second))


# Creating Buttons for Calcualtor with Some Basic Keys
button_1=Button(root,text="7",padx="40",pady="20",command=lambda:button_click(7),border=10,fg="Black")
button_1.grid(row="3",column="0")

button_2=Button(root,text="8",padx="40",pady="20",command=lambda:button_click(8),border=10,fg="Black")
button_2.grid(row="3",column="1")

button_3=Button(root,text="9",padx="40",pady="20",command=lambda:button_click(9),border=10,fg="Black")
button_3.grid(row="3",column="2")

button_4=Button(root,text="4",padx="40",pady="20",command=lambda:button_click(4),border=10,fg="Black")
button_4.grid(row="4",column="0")

button_5=Button(root,text="5",padx="40",pady="20",command=lambda:button_click(5),border=10,fg="Black")
button_5.grid(row="4",column="1")

button_6=Button(root,text="6",padx="40",pady="20",command=lambda:button_click(6),border=10,fg="Black")
button_6.grid(row="4",column="2")

button_7=Button(root,text="1",padx="40",pady="20",command=lambda:button_click(1),border=10,fg="Black")
button_7.grid(row="5",column="0")

button_8=Button(root,text="2",padx="40",pady="20",command=lambda:button_click(2),border=10,fg="Black")
button_8.grid(row="5",column="1")

button_9=Button(root,text="3",padx="40",pady="20",command=lambda:button_click(3),border=10,fg="Black")
button_9.grid(row="5",column="2")

button_0=Button(root,text="0",padx="40",pady="20",command=lambda:button_click(0),border=10,fg="Black")
button_0.grid(row="6",column="1")

button_plus=Button(root,text="+",padx="40",pady="20",command=button_add,border=10,fg="Black")
button_plus.grid(row="6",column="0")

button_min=Button(root,text="__",padx="40",pady="20",command=button_minus,border=10,fg="Black")
button_min.grid(row=7,column=0)
button_mul=Button(root,text="X",padx="40",pady="20",command=button_multiply,border=10,fg="Black")
button_mul.grid(row=7,column=1)

button_div=Button(root,text="/",padx="40",pady="20",command=button_divide,border=10,fg="Black")
button_div.grid(row=7,column=2)

button_dot=Button(root,text=".",padx="40",pady="20",command=lambda:button_click("."),border=10,fg="Black")
button_dot.grid(row="6",column="2")

button_Clear=Button(root,text="Clear",padx="150",pady="25",command=button_clear,border=10,fg="Black")
button_Clear.grid(row=1,column=0,columnspan=3)

button_equal=Button(root,text="=",padx="150",pady="25",command=Equal,border=10,fg="Black")
button_equal.grid(row=8,column=0,columnspan="3")


root.mainloop()
