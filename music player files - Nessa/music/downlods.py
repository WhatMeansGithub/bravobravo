import requests
import os

# Function to download music from a URL
def download_music(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print("Failed to download music:", response.status_code)
        return False

# Example URL of the music you want to download
music_url = "http://www.naijapals.com/music/T_shirt_Shontelle-4401"

# Directory to save the downloaded music
save_music= "downloads"

# Ensure the directory exists
if not os.path.exists(save_music):
    os.makedirs(save_music)

# Extract filename from the URL
filename = os.path.basename(music_url)

# Save path for the downloaded music
save_path = os.path.join(save_music,filename )

# Download the music
if download_music(music_url, save_path):
    print("Music downloaded successfully to:", save_path)
else:
    print("Failed to download music.")
