import tkinter as tk
import pygame.mixer
from tkinter import filedialog
from tkinter.ttk import Progressbar
import customtkinter as ctk
from mutagen.mp3  import MP3
import threading
import time
import os

# creating the window
window = tk.Tk()
window.title("BeatBliss Music Player App")
window.geometry("600x500")

#creating a label for the usic playr title
label_music_player = tk.Label(window, text ="BeatBliss Player", front= ("TkDefaultFont"))
label_music_player.pack(pady=10)