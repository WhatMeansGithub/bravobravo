import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
from PIL import Image, ImageTk
import os
import pygame
import threading
import time
from mutagen.mp3 import MP3
from googleapiclient.discovery import build
from pytube import YouTube
from moviepy.editor import AudioFileClip

# Initialize pygame mixer
pygame.mixer.init()

# Set appearance mode and default color theme
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

# Global variables
list_of_songs = []
list_of_covers = []
n = 0
paused = False

# Function to clear entry fields
def clear_entries(*entries):
    for entry in entries:
        entry.delete(0, tk.END)

# Function to display cover and song name
def display_cover_and_name(song_index):
    cover_path = list_of_covers[song_index % len(list_of_covers)]
    song_name = os.path.basename(list_of_songs[song_index])
    img = Image.open(cover_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    load = ImageTk.PhotoImage(img)

    global label1
    try:
        label1.destroy()
    except NameError:
        pass

    label1 = customtkinter.CTkLabel(music_player, image=load)
    label1.image = load
    label1.place(relx=0.23, rely=0.13)

    stripped_string = os.path.splitext(song_name)[0]
    song_name_label = customtkinter.CTkLabel(music_player, text=stripped_string, bg_color='#222222', text_color='white')
    song_name_label.place(relx=.3, rely=.9)

# Function to play music
def play_music(song_index=None):
    global n 
    if song_index is not None:
        n = song_index
    pygame.mixer.music.load(list_of_songs[n])
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(.5)
    display_cover_and_name(n)
    progressbar_thread = threading.Thread(target=update_progress)
    progressbar_thread.daemon = True
    progressbar_thread.start()

# Function to pause music
def pause_music():
    pygame.mixer.music.pause()

# Function to stop music
def stop_music():
    global paused
    pygame.mixer.music.stop()
    paused = False

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
    song_len = MP3(list_of_songs[n]).info.length
    while pygame.mixer.music.get_busy():
        current_pos = pygame.mixer.music.get_pos() / 1000
        pbar.set(current_pos / song_len * 100)
        time.sleep(0.1)

# Function to adjust the volume
def volume(value):
    pygame.mixer.music.set_volume(value)

# Function to open music player window
def open_music_player():
    global music_player, list_of_songs, list_of_covers, n, pbar, lbox
    root.destroy()  # Close the root window when the music player is opened
    music_player = customtkinter.CTk()
    music_player.title("Vibe Box")
    music_player.geometry('600x500')

    # Add background image
    bg_image = Image.open('Nessa/img/3d-music.jpg')
    bg_image = bg_image.resize((600, 500), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(music_player, image=bg_photo)
    bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    bg_label.image = bg_photo

    # Update global variables
    list_of_songs = [os.path.join('Nessa/music', file) for file in os.listdir('Nessa/music') if file.endswith(".mp3")]
    list_of_covers = ['Nessa/img/colorful-music-note.jpg', 'Nessa/img/headimg.jpg', 'Nessa/img/beautiful-robotic-woman-listening.jpg', 'Nessa/img/person-listen-music.jpg', 'Nessa/img/music-note.jpg', 'Nessa/img/beautiful-robotic-woman-listening.jpg']
    n = 0

    
    # Function to handle song selection from dropdown
    def on_song_selected(event):
        selected_song = song_listbox.get(song_listbox.curselection())
        song_index = list_of_songs.index(selected_song)
        play_music(song_index)

    # Function to open dropdown list in a new window
    def open_dropdown():
        dropdown_window = tk.Toplevel(music_player)
        dropdown_window.title("Select Song")
        dropdown_window.geometry("300x400")

        scrollbar = tk.Scrollbar(dropdown_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        global song_listbox
        song_listbox = tk.Listbox(dropdown_window, yscrollcommand=scrollbar.set)
        for song in list_of_songs:
            song_listbox.insert(tk.END, os.path.basename(song))
        song_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=song_listbox.yview)

        song_listbox.bind("<<ListboxSelect>>", on_song_selected)

    dropdown_button = customtkinter.CTkButton(master=music_player, text="Select Music", command=open_dropdown)
    dropdown_button.place(relx=0.01, rely=0.01, anchor=tk.NW)

   

    play_button = customtkinter.CTkButton(master=music_player, text='Play', command=play_music, width=5)
    play_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    
    pause_button = customtkinter.CTkButton(master=music_player, text='Pause', command=pause_music, width=5)
    pause_button.place(relx=0.4, rely=0.7, anchor=tk.CENTER)
    
    skip_b = customtkinter.CTkButton(master=music_player, text='<', command=play_previous_music, width=5)
    skip_b.place(relx=0.3, rely=0.7, anchor=tk.CENTER)
    
    skip_f = customtkinter.CTkButton(master=music_player, text='>', command=play_next_music, width=5)
    skip_f.place(relx=0.6, rely=0.7, anchor=tk.CENTER)
    
    slider = customtkinter.CTkSlider(master=music_player, from_=0, to=1, command=volume, width=210)
    slider.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

    pbar = customtkinter.CTkProgressBar(master=music_player)
    pbar.place(relx=.5, rely=.85, anchor=tk.CENTER)

    lbox = tk.Listbox(music_player)
    lbox.place(relx=0.5, rely=0.9, anchor=tk.LEFT)

    for song in list_of_songs:
        lbox.insert(tk.END, os.path.basename(song))

    def play_selected_song(event):
        selected_index = lbox.curselection()[0]
        play_music(selected_index)
    
    lbox.bind('<Double-1>', play_selected_song)

    music_player.mainloop()

# Function to select music folder
def select_music_folder():
    global list_of_songs
    selected_folder_path = filedialog.askdirectory()
    if selected_folder_path:
        list_of_songs = [os.path.join(selected_folder_path, file) for file in os.listdir(selected_folder_path) if file.endswith(".mp3")]
        lbox.delete(0, tk.END)
        for song in list_of_songs:
            lbox.insert(tk.END, os.path.basename(song))

# Function to download music from YouTube and convert to MP3
def download_music(url, save_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
        return True
    except Exception as e:
        print("Failed to download music:", e)
        return False

# Function to convert MP4 to MP3
def convert_to_mp3(mp4_path, mp3_path):
    try:
        audio_clip = AudioFileClip(mp4_path)
        audio_clip.write_audiofile(mp3_path)
        audio_clip.close()
        return True
    except Exception as e:
        print("Failed to convert to MP3:", e)
        return False

# YouTube API key and service setup
YOUTUBE_API_KEY = 'AIzaSyC-Y94FbyMgf7tKC-kjBUuuIDkWM-_MMcI'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Function to search music online using YouTube API
def search_music_online():
    search_query = search_entry.get()
    request = youtube.search().list(
            part="snippet",
            maxResults=10,
            q=search_query,
            type="video",
            videoCategoryId="10"  # Music category
        )
    response = request.execute()
    search_results = [(item['snippet']['title'], f"https://www.youtube.com/watch?v={item['id']['videoId']}") for item in response['items']]
    display_search_results(search_results)

# Function to display search results
def display_search_results(results):
    search_results_window = customtkinter.CTkToplevel(root)
    search_results_window.title("Search Results")
    search_results_window.geometry("400x300")

    for idx, (song_name, url) in enumerate(results):
        result_label = customtkinter.CTkLabel(search_results_window, text=song_name)
        result_label.pack(pady=2)
        download_button = customtkinter.CTkButton(search_results_window, text="Download", command=lambda url=url: download_and_convert(url))
        download_button.pack(pady=2)

# Function to download and convert music
def download_and_convert(url):
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        mp4_path = file_path.replace(".mp3", ".mp4")
        if download_music(url, mp4_path):
            if convert_to_mp3(mp4_path, file_path):
                os.remove(mp4_path)
                messagebox.showinfo("Success", "Download and conversion successful!")
            else:
                messagebox.showerror("Error", "Failed to convert to MP3")
        else:
            messagebox.showerror("Error", "Failed to download music")

# Main application window
root = customtkinter.CTk()
root.title("Music Application")
root.geometry("1200x800+400+150")                                 # Setting the fixed size and position of the window

search_label = customtkinter.CTkLabel(root, text="Search Music Online:")
search_label.pack(pady=10)
search_entry = customtkinter.CTkEntry(root)
search_entry.pack(pady=10)
search_button = customtkinter.CTkButton(root, text="Search", command=search_music_online)
search_button.pack(pady=10)

download_label = customtkinter.CTkLabel(root, text="Download and Convert Music:")
download_label.pack(pady=10)
url_entry = customtkinter.CTkEntry(root, placeholder_text="Enter YouTube URL")
url_entry.pack(pady=10)
download_button = customtkinter.CTkButton(root, text="Download", command=lambda: download_and_convert(url_entry.get()))
download_button.pack(pady=10)

open_music_player_button = customtkinter.CTkButton(root, text="Open Music Player", command=open_music_player)
open_music_player_button.pack(pady=10)

#root.mainloop()















root.mainloop()