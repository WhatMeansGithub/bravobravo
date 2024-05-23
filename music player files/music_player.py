import tkinter as tk
import customtkinter 
import pygame
from PIL import Image,ImageTk
from threading import Thread
import time
import math
import os
# Set appearance mode and default color theme
customtkinter.set_appearance_mode("System")   #Modes: sytem (default.light,dark)
customtkinter.set_default_color_theme("green")   #themes :blue (default), dark-blue,green


root = customtkinter.CTk()
root.title("vibe Box")
root.geometry('400x480')
pygame.mixer.init()


# Path to the music folder
music_folder = 'Nessa/music/'

# List of songs and covers
list_of_songs = [music_folder + 'Ayra-Starr-Commas.mp3', music_folder + 'Akwaboah-Jnr-Mesan-Agye-Wo-Live-session.mp3']
list_of_covers = ['Nessa/img/colorful-music-note.jpg', 'Nessa/img/headimg.jpg','Nessa/img/beautiful-robotic-woman-listening.jpg', 'Nessa/img/person-listen-music.jpg', 'Nessa/img/music-note.jpg', 'Nessa/img/beautiful-robotic-woman-listening.jpg']
n = 0


# Function to display cover and song name
def display_cover_and_name(song_index):
    cover_path = list_of_covers[song_index]
    song_name = os.path.basename(list_of_songs[song_index])
    img = Image.open(cover_path)
    print(img)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    load = ImageTk.PhotoImage(img)
    label1 = tk.Label(root, image=load)
    label1.image = load
    label1.place(relx=0.19, rely=0.06)
    stripped_string = os.path.splitext(song_name)[0]
    song_name_label = tk.Label(text=stripped_string, bg='#222222', fg='blue')
    song_name_label.place(relx=.4, rely=.6)


# Function to play music
def play_music():
    global n
    pygame.mixer.music.load(list_of_songs[n])
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(.5)
    display_cover_and_name(n)
    progressbar_thread = Thread(target=update_progress)
    progressbar_thread.daemon = True
    progressbar_thread.start()


# Function to pause music
def pause():
     global paused
     pygame.mixer.music.pause()
     paused = True


# Function to play the next music
def play_next_music():
    global n
    n = (n + 1) % len(list_of_songs)
    play_music()


# Function to play the previous music
def play_previous_music():
    global n
    n = (n - 1) % len(list_of_songs)
    play_music()


# Function to update the progress bar
def update_progress():
    song_len = pygame.mixer.Sound(list_of_songs[n]).get_length()
    while pygame.mixer.music.get_busy():
        current_pos = pygame.mixer.music.get_pos() / 1000
        pbar.set(current_pos / song_len * 100)
        time.sleep(0.1)


# Function to adjust the volume
def volume(value):
    pygame.mixer.music.set_volume(value)


#buttonss
play_button =customtkinter.CTkButton(master=root, text='play', command=play_music,width=5)
play_button.place(relx=0.5, rely=0.7,anchor=tk.CENTER, )

pause=customtkinter.CTkButton(master=root, text='pause', command=pause, width=5)
pause.place(relx=0.4, rely=0.7,anchor=tk.CENTER)

skip_b=customtkinter.CTkButton(master=root, text='<', command=play_previous_music, width=5)
skip_b.place(relx=0.3, rely=0.7,anchor=tk.CENTER)

skip_f=customtkinter.CTkButton(master=root, text='>', command=play_next_music, width=5)
skip_f.place(relx=0.6, rely=0.7,anchor=tk.CENTER)

slider =customtkinter.CTkSlider(master=root, from_= 0, to=1, command=volume, width=210)
slider.place(relx=0.5, rely=0.78,anchor=tk.CENTER)


#creating a lisbox to display available songs
lbox = tk.Listbox(master=root)
lbox.pack(pady=10)

#creating a bar to indicate the current songs progress
pbar = customtkinter.CTkProgressBar(master=root)
pbar.place(relx=.5, rely=.85,anchor=tk.CENTER)















root.mainloop()