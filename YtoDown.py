import time
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
from shutil import move, rmtree


def download_video(url, output_path):
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

        print(f"Downloaded video as MP4: {video_file}")
        time.sleep(2.4)  # Opóźnienie na potrzeby obserwacji

        return video_file

    except Exception as e:
        print(f"An error occurred during video download: {e}")
        return None


def convert_to_mp3(video_file, output_path):
    try:
        # Convert MP4 to MP3
        print("Converting to MP3...")
        mp3_file = os.path.join(
            output_path, f"{os.path.splitext(os.path.basename(video_file))[0]}.mp3")
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(mp3_file)
        clip.close()

        print(f"Converted video to MP3: {mp3_file}")
        time.sleep(2.4)  # Opóźnienie na potrzeby obserwacji

        return mp3_file

    except Exception as e:
        print(f"An error occurred during MP3 conversion: {e}")
        return None


def move_to_downloads(mp3_file):
    try:
        # Move the MP3 file to the user's "Downloads" folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        downloads_mp3_file = os.path.join(
            downloads_path, os.path.basename(mp3_file))
        move(mp3_file, downloads_mp3_file)

        print(f"Moved MP3 file to Downloads: {downloads_mp3_file}")
        time.sleep(2.4)  # Opóźnienie na potrzeby obserwacji

    except Exception as e:
        print(f"An error occurred during file move: {e}")


def cleanup(output_path, mp3_file):
    try:
        # Remove the MP4 file and the output folder
        os.remove(os.path.join(output_path, f"{
                  os.path.splitext(os.path.basename(mp3_file))[0]}.mp4"))
        rmtree(output_path)

        print("Cleanup done: Removed MP4 and output folder.")
        time.sleep(2.4)  # Opóźnienie na potrzeby obserwacji

    except Exception as e:
        print(f"An error occurred during cleanup: {e}")


if __name__ == "__main__":
    # Set the path to the folder where files will be saved
    output_folder = os.path.join(os.path.dirname(__file__), "output")

    # Input YouTube URL
    youtube_url = input("Enter the YouTube URL: ")

    # Download and convert video
    video_file = download_video(youtube_url, output_folder)

    if video_file:
        mp3_file = convert_to_mp3(video_file, output_folder)
        if mp3_file:
            move_to_downloads(mp3_file)
            cleanup(output_folder, mp3_file)
