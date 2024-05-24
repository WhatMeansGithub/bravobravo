import tkinter as tk                    # Importing tkinter as tk to create the GUI
import tkinter.ttk as ttk               # Does the same as 'from tkinter import ttk' but lets us customize the GUI even more with themes
import ttkbootstrap as ttk              # Does the same as 'from tkinter import ttk' but lets us customize the GUI even more with themes
from tkinter import font as tkFont      # Importing font as tkFont to customize the font of the GUI
from PIL import Image, ImageTk          # Importing Image and ImageTk from PIL to display images in the GUI
import customtkinter as ctk


root = ctk.CTk()  # Creating a tkinter window
root.wm_attributes('-alpha', 0.9)  # Set window transparency to 90%

root.title("The CEO Program")  # Setting the title of the window
root.geometry("1200x800")  # Setting the fixed size of the window
root.resizable(False, False)  # Disabling window resizing




# Creating a label widget to display the background image
background_image = 'program files/main_page_background.jpg'
img = Image.open(background_image)
img = ImageTk.PhotoImage(img)
img_label = ttk.Label(root, image=img)
img_label.place(x=-2, y=-2, relwidth=1, relheight=1)  # Place the image label to cover the entire window



# Creating a frame widget to hold the buttons and customizing them
buttons = ["Employees", "Market", "Music", "Exit"]
button_frame = ttk.Frame(root)  
button_frame.place(relx=1, rely=0.5, anchor='e')  

# Placing the buttons in the button frame widget and customizing it
for text in buttons:
    button = ctk.CTkButton(button_frame, text=text, width=250, height=100, anchor='center')  
    button.pack(padx=32, pady=(52)) 

root.mainloop()

