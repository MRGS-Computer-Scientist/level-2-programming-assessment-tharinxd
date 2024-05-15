from tkinter import *

w_width = 500
w_height = 700

window = Tk()
window.geomerty(str(w_width) + "n" + str(w_height))
window.title("My app")

main_frame = Frame(background= "red" , width=w_width, height= w_height)
main_frame.pack()

hello_label = Label(text= "Hello Bilal")
hello_label.grid(column=0, row=0)


window.mainloop()

