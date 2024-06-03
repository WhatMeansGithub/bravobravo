from tkinter import *
from pytube import YouTube
import customtkinter
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import os
from yt_dlp import YoutubeDL

customtkinter.set_appearance_mode("light")  
customtkinter.set_default_color_theme("green")

def select_directory():
    global directory_path
    directory_path = filedialog.askdirectory()
    if directory_path:
        messagebox.showinfo("Directory Selected", f"Files will be saved to: {directory_path}")
def download_video():
    url = url_entry.get()
    if url and directory_path:
        try:
            ydl_opts = {
                'format': 'best', 
                'outtmpl': os.path.join(directory_path, '%(title)s.%(ext)s'),
                'postprocessors': [{  
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4', }],}
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                messagebox.showinfo("Download", "Downloaded Successfully")
        except Exception as e:
            print(f"An error occurred: {str(e)}")  
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showwarning("Input Required", "Please provide a valid URL and select a directory.")

def download_audio():
     url = url_entry.get()
     if url and directory_path:
        try:
            ydl_opts = {
                'format': 'best', 
                'outtmpl': os.path.join(directory_path, '%(title)s.%(ext)s'),
                'postprocessors': [{ 
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp3',}],}
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                messagebox.showinfo("Download", "Downloaded Successfully")
        except Exception as e:
            print(f"An error occurred: {str(e)}")  
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
     else:
        messagebox.showwarning("Input Required", "Please provide a valid URL and select a directory.")

root=customtkinter.CTk()
root.geometry("900x700")
root.title("YouTube Video Downloader")

img=ImageTk.PhotoImage(Image.open("yt.jpg"))
im1=customtkinter.CTkLabel(root,image=img)
im1.pack()

Frame=customtkinter.CTkFrame(master=root , width=500, height=600,border_color="#CD3131",border_width=0)
Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

url_label = customtkinter.CTkLabel(master=Frame, text="YouTube URL:")
url_label.grid(row=0, column=0, padx=10, pady=5)
url_entry = customtkinter.CTkEntry(master=Frame, width=400)
url_entry.grid(row=0, column=1, padx=10, pady=5)
select_button = customtkinter.CTkButton(master=Frame, text="Select Directory", command=select_directory,fg_color="#750000",hover_color="firebrick4",corner_radius=8)
select_button.grid(row=1, column=0, columnspan=2, pady=10)

download_button = customtkinter.CTkButton(master=Frame, text="Download Video", command=download_video,fg_color="firebrick4",hover_color="#750000",corner_radius=8)
download_button.grid(row=4, column=0, columnspan=2, pady=10)
audio_button = customtkinter.CTkButton(master=Frame, text="Download Audio", command=download_audio,fg_color="firebrick4",hover_color="#750000",corner_radius=8)
audio_button.grid(row=5, column=0, columnspan=2, pady=10)
directory_path = "" 

root.mainloop()
