import tkinter
from tkinter import *
from PIL import ImageTk, Image
import customtkinter
from tkinter import messagebox
from tkinter import filedialog
import os
import subprocess
customtkinter.set_appearance_mode("light")  
customtkinter.set_default_color_theme("green")


def open_employees():
    root.withdraw()
    subprocess.Popen(['/usr/bin/python3', '2._employees.py'])
    root.withdraw()
def open_music():
    root.withdraw()
    subprocess.Popen(['/usr/bin/python3', '4._music_player_Nessa.py'])

def open_market():
    root.withdraw()
    os.system('python market.py')

root = customtkinter.CTk()
root.geometry("900x700")
root.title("Music Player")


img=ImageTk.PhotoImage(Image.open("yt.jpg"))
im1=customtkinter.CTkLabel(root,image=img)
im1.pack()


Frame=customtkinter.CTkFrame(master=root , width=500, height=600,border_color="#CD3131",border_width=0)
Frame.place(relx=0.5, rely=0.5, anchor=CENTER)



Label1=customtkinter.CTkLabel(master=Frame, text="welcome to Bravo,Bravo", font=("Arial", 20))
Label1.pack(pady=20,padx=20)


Button1=customtkinter.CTkButton(master=Frame, text="Empolyees",fg_color="firebrick4",hover_color="#750000",corner_radius=8,command=open_employees)
Button1.pack(pady=20,padx=20)


Button2=customtkinter.CTkButton(master=Frame, text="Music",fg_color="firebrick4",hover_color="#750000",corner_radius=8,command=open_music)
Button2.pack(pady=20,padx=20)

Button3=customtkinter.CTkButton(master=Frame, text="Marketing",fg_color="firebrick4",hover_color="#750000",corner_radius=8,command=open_market)
Button3.pack(pady=20,padx=20)

Button4=customtkinter.CTkButton(master=Frame, text="E X I T",fg_color="firebrick4",hover_color="#750000",corner_radius=8,command=root.destroy)
Button4.pack(pady=20,padx=20)












root.mainloop()