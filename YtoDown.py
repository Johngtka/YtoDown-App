import os
import tkinter as tk
from pytube import YouTube
from moviepy.editor import VideoFileClip
from shutil import move, rmtree
import time


def download_and_convert_video(url, output_path, status_label, result_label, window):
    try:
        # Download the YouTube video as an MP4 file
        youtube = YouTube(url)
        video_stream = youtube.streams.filter(file_extension='mp4').first()

        # Check if the output directory exists, if not, create it
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Download video as an MP4 file
        video_file = os.path.join(output_path, f"{video_stream.title}.mp4")
        video_stream.download(output_path, video_file)

        status_label.config(text=f"Downloaded video as MP4: {video_file}")
        window.update()

        time.sleep(3)  # 3-second delay

        # Convert MP4 to MP3
        status_label.config(text="Converting to MP3...", fg="#87AE73")  # Sage
        window.update()

        time.sleep(3)  # 3-second delay

        mp3_file = os.path.join(output_path, f"{video_stream.title}.mp3")
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(mp3_file)
        clip.close()

        status_label.config(text=f"Converted video to MP3: {
                            mp3_file}", fg="#F3E5AB")  # Vanilla
        window.update()

        time.sleep(3)  # 3-second delay

        result_label.config(text=f"MP3 file available at:\n{os.path.join(os.path.expanduser(
            '~'), 'Downloads', os.path.basename(mp3_file))}", fg="#D2B48C")

        window.update()

        return mp3_file

    except Exception as e:
        status_label.config(text=f"An error occurred: {
                            e}", fg="#C08080")  # Old Rose
        window.update()
        return None


def move_to_downloads_and_cleanup(mp3_file, output_path, status_label, result_label, window):
    try:
        # Move the MP3 file to the user's "Downloads" folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        downloads_mp3_file = os.path.join(
            downloads_path, os.path.basename(mp3_file))
        move(mp3_file, downloads_mp3_file)

        status_label.config(text=f"Moved MP3 file to Downloads: {
                            downloads_mp3_file}", fg="#F5F5DC")  # Beige
        window.update()

        time.sleep(3)  # 3-second delay

        # Remove the MP4 file and the output folder
        os.remove(os.path.join(output_path, f"{
                  os.path.splitext(os.path.basename(mp3_file))[0]}.mp4"))
        rmtree(output_path)

        status_label.config(
            text="Cleanup done: Removed MP4 and output folder.", fg="#D2B48C")  # Buff
        result_label.config(text="", fg="#D2B48C")  # Buff
        window.update()

    except Exception as e:
        status_label.config(text=f"An error occurred during cleanup: {
                            e}", fg="#C08080")  # Old Rose
        window.update()


def on_download_button_click():
    youtube_url = entry.get()

    if not youtube_url:
        result_label.config(text="Enter a YouTube URL.",
                            fg="#C08080")  # Old Rose
        window.update()
        return

    # Set the path to the folder where files will be saved
    output_folder = os.path.join(os.path.dirname(__file__), "output")

    # Clear previous status
    status_label.config(text="", fg="#87AE73")  # Sage
    result_label.config(text="", fg="#D2B48C")  # Buff
    window.update()

    mp3_file = download_and_convert_video(
        youtube_url, output_folder, status_label, result_label, window)

    if mp3_file:
        move_to_downloads_and_cleanup(
            mp3_file, output_folder, status_label, result_label, window)


# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("400x200")
window.configure(bg="#F5F5DC")  # Beige

# Create and place the entry widget for the YouTube URL
entry = tk.Entry(window, width=40, bg="#FFE4C4")  # Buff
entry.grid(row=0, column=0, padx=10, pady=10)

# Create and place the download button
download_button = tk.Button(
    # Vanilla, Old Rose
    window, text="Download", command=on_download_button_click, bg="#F3E5AB", fg="#C08080")
download_button.grid(row=0, column=1, padx=10, pady=10)

# Create and place the result label
result_label = tk.Label(window, text="", fg="#D2B48C",
                        bg="#F5F5DC")  # Buff, Beige
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Create and place the status label
status_label = tk.Label(window, text="", fg="#87AE73",
                        bg="#F5F5DC")  # Sage, Beige
status_label.grid(row=1, column=0, columnspan=2, pady=10)

# Start
window.mainloop()
