import tkinter as tk                    # Importing tkinter as tk to create the GUI
import ttkbootstrap as ttk              # Does the same as 'from tkinter import ttk' but lets us customize the GUI even more with themes


root = ttk.Window(themename = 'darkly') # Creating a tkinter window and customising it
root.title("Main Page")                 # Setting the title of the window
root.geometry("1200x800")               # Setting the fixed size of the window
root.resizable(False, False)            # Disabling window resizing
root.background = 'black'               # Setting the background color of the window

# Creating a frame widget to hold the buttons
buttons = [
    ("Employees"),
    ("Market"),
    ("Music"),
    ("Exit"),
]
button_frame = ttk.Frame(root)
button_frame.pack(anchor='center', padx=15, pady=10)
button_frame.pack(pady=20)  # Displaying the frame widget
for text in buttons:
    ttk.Button(button_frame, text=text).pack(anchor='center', padx=5, pady=5) 
button_frame.pack(pady=300)  # Displaying the frame widget

# Creating a label widget to display the background image
img= tk.PhotoImage(file='background', master=root)
img_label = ttk.Label(root, image=img)
img_label.pack(fill='both', expand=True)

root.mainloop()