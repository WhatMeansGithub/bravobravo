import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
from PIL import Image, ImageTk
import os
import json
import pygame
import threading
import time
import requests
from mutagen.mp3 import MP3
from googleapiclient.discovery import build
from pytube import YouTube
from moviepy.editor import AudioFileClip

# Initialize pygame mixer
pygame.mixer.init()

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
    label1.place(relx=0.19, rely=0.06)

    stripped_string = os.path.splitext(song_name)[0]
    song_name_label = customtkinter.CTkLabel(music_player, text=stripped_string, bg_color='#222222', text_color='white')
    song_name_label.place(relx=.4, rely=.6)

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
    global music_player, list_of_songs, list_of_covers, n
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

    # Back button to return to the main page
    def back_to_main():
        music_player.destroy()
        main()

    back_button = customtkinter.CTkButton(master=music_player, text="< Back", command=back_to_main)
    back_button.place(relx=0.02, rely=0.02, anchor=tk.NW)

    select_folder_button = customtkinter.CTkButton(master=music_player, text="Select Music Folder", command=select_music_folder, width=5)
    select_folder_button.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

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

    global pbar
    pbar = customtkinter.CTkProgressBar(master=music_player)
    pbar.place(relx=.5, rely=.85, anchor=tk.CENTER)

    global lbox
    lbox = tk.Listbox(music_player)
    lbox.place(relx=0.5, rely=0.9, anchor=tk.LEFT)

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
    if search_query:
        request = youtube.search().list(
            part="snippet",
            maxResults=10,
            q=search_query,
            type="video",
            videoCategoryId="10"  # Music category
        )
        response = request.execute()
        search_results = [(item['snippet']['title'], f"https://www.youtube.com/watch?v={item['id']['videoId']}") for item in response.get('items', [])]
        display_search_results(search_results)

# Function to display search results and allow downloading
def display_search_results(results):
    search_results_window = customtkinter.CTkToplevel(root)
    search_results_window.title("Search Results")
    search_results_window.geometry("400x300")
    
    for idx, (song_name, song_url) in enumerate(results):
        result_label = customtkinter.CTkLabel(master=search_results_window, text=song_name)
        result_label.grid(row=idx, column=0, pady=5, padx=5)
        
        download_button = customtkinter.CTkButton(master=search_results_window, text="Download", command=lambda url=song_url, name=song_name: download_and_add_to_playlist(url, name))
        download_button.grid(row=idx, column=1, pady=5, padx=5)

def download_and_add_to_playlist(url, song_name):
    save_directory = "downloads"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    mp4_filename = f"{song_name}.mp4"
    mp3_filename = f"{song_name}.mp3"
    mp4_path = os.path.join(save_directory, mp4_filename)
    mp3_path = os.path.join(save_directory, mp3_filename)

    if download_music(url, mp4_path):
        if convert_to_mp3(mp4_path, mp3_path):
            os.remove(mp4_path)  # Remove the MP4 file after conversion
            messagebox.showinfo("Success", f"{song_name} downloaded and converted to MP3 successfully!")
            list_of_songs.append(mp3_path)
            lbox.insert(tk.END, song_name)
        else:
            messagebox.showerror("Error", f"Failed to convert {song_name} to MP3.")
    else:
        messagebox.showerror("Error", f"Failed to download {song_name}.")

# Function to open the downloads and playlist window
def open_downloads_playlist():
    global downloads_window, bg_label_playlist, dropdown

    downloads_window = customtkinter.CTk()
    downloads_window.title("Downloads and Playlist")
    downloads_window.geometry("600x540")

    # Add background image
    bg_image_playlist = Image.open('Nessa/img/3d-music.jpg')
    bg_image_playlist = bg_image_playlist.resize((600, 540), Image.Resampling.LANCZOS)
    bg_photo_playlist = ImageTk.PhotoImage(bg_image_playlist)

    bg_label_playlist = tk.Label(downloads_window, image=bg_photo_playlist)
    bg_label_playlist.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    bg_label_playlist.image = bg_photo_playlist

    # Back button to return to the main page
    def back_to_main():
        downloads_window.destroy()
        main()

    back_button = customtkinter.CTkButton(master=downloads_window, text="< Back", command=back_to_main)
    back_button.place(relx=0.02, rely=0.02, anchor=tk.NW)

    listbox = tk.Listbox(downloads_window)
    listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    for idx, song in enumerate(list_of_songs):
        listbox.insert(tk.END, os.path.basename(song))

    def play_selected_song(event):
        selected_index = listbox.curselection()[0]
        play_music(selected_index)
    
    listbox.bind('<Double-1>', play_selected_song)

    play_button_playlist = customtkinter.CTkButton(master=downloads_window, text='Play', command=play_music, width=5)
    play_button_playlist.place(relx=0.4, rely=0.9, anchor=tk.CENTER)
    
    pause_button_playlist = customtkinter.CTkButton(master=downloads_window, text='Pause', command=pause_music, width=5)
    pause_button_playlist.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    
    skip_b_playlist = customtkinter.CTkButton(master=downloads_window, text='<', command=play_previous_music, width=5)
    skip_b_playlist.place(relx=0.3, rely=0.9, anchor=tk.CENTER)
    
    skip_f_playlist = customtkinter.CTkButton(master=downloads_window, text='>', command=play_next_music, width=5)
    skip_f_playlist.place(relx=0.6, rely=0.9, anchor=tk.CENTER)
    
    slider_playlist = customtkinter.CTkSlider(master=downloads_window, from_=0, to=1, command=volume, width=210)
    slider_playlist.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    downloads_window.mainloop()

# Function to launch the main window
def main():
    global root, search_entry
    root = customtkinter.CTk()
    root.title("Vibe Box")
    root.geometry("600x540")

    # Background  image the main window
    img = ImageTk.PhotoImage(Image.open("Nessa/img/beautiful-robotic-woman-listening.jpg"))
    i1 = customtkinter.CTkLabel(master=root, image=img)
    i1.pack()

    frame = customtkinter.CTkFrame(master=root, width=300, height=350, corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    l1 = customtkinter.CTkLabel(master=frame, text="Vibe Box", font=("microsoft yahei", 24), text_color="#87c423")
    l1.place(x=50, y=45)

    search_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Search Music Online", height=40, width=200, corner_radius=20, border_width=0, fg_color="black")
    search_entry.place(x=50, y=110)

    search_button = customtkinter.CTkButton(master=frame, text="Search", font=("microsoft yahei", 12), height=30, width=140, corner_radius=20, command=search_music_online, fg_color="#87c423", text_color="#01120d", border_width=0, hover_color="#15A911", cursor="hand2")
    search_button.place(x=84, y=170)

    open_player_button = customtkinter.CTkButton(master=frame, text="Open Music Player", font=("microsoft yahei", 12), height=30, width=140, corner_radius=20, command=open_music_player, fg_color="#87c423", text_color="#01120d", border_width=0, hover_color="#15A911", cursor="hand2")
    open_player_button.place(x=84, y=230)

    open_downloads_button = customtkinter.CTkButton(master=frame, text="Downloads and Playlist", font=("microsoft yahei", 12), height=30, width=140, corner_radius=20, command=open_downloads_playlist, fg_color="#87c423", text_color="#01120d", border_width=0, hover_color="#15A911", cursor="hand2")
    open_downloads_button.place(x=84, y=290)

    root.mainloop()

if __name__ == "__main__":
    main()
