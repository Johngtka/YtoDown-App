import os
import sys
import time
from pytube import YouTube
from shutil import move, rmtree
from moviepy.editor import VideoFileClip

SLEEP_DURATION = 2


def print_with_spacing(message):
    print(f"\n{message}\n")


def loading_animation():
    for _ in range(5):
        sys.stdout.write("\rProcessing, Please wait.   ")
        time.sleep(0.2)
        sys.stdout.write("\rProcessing, Please wait..  ")
        time.sleep(0.2)
        sys.stdout.write("\rProcessing, Please wait... ")
        time.sleep(0.2)
    sys.stdout.write("\r")


def download_video(url, output_path):
    try:
        youtube = YouTube(url)

        if youtube.age_restricted:
            print_with_spacing(
                "This video is age restricted. Please log in to download.")
            return None

        video_stream = youtube.streams.filter(file_extension='mp4').first()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        video_title = "".join(c if c.isalnum() or c in [
                              ' ', '.', '-', '_'] else '_' for c in video_stream.title)

        video_file = os.path.join(output_path, f"{video_title}.mp4")
        video_stream.download(output_path, video_file)

        print_with_spacing(f"Downloaded video as MP4: {video_file}")
        time.sleep(SLEEP_DURATION)

        return video_file

    except Exception as e:
        print_with_spacing(f"An error occurred during video download: {e}")
        return None


def convert_to_mp3(video_file, output_path):
    try:
        print_with_spacing("Converting to MP3...")
        loading_animation()
        mp3_file = os.path.join(
            output_path, f"{os.path.splitext(video_file)[0]}.mp3")
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(mp3_file)
        clip.close()

        print_with_spacing(f"Converted video to MP3: {mp3_file}")
        time.sleep(SLEEP_DURATION)

        return mp3_file

    except Exception as e:
        print_with_spacing(f"An error occurred during MP3 conversion: {e}")
        return None


def move_to_downloads(mp3_file):
    try:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        downloads_mp3_file = os.path.join(
            downloads_path, os.path.basename(mp3_file))
        move(mp3_file, downloads_mp3_file)

        print_with_spacing(f"Moved MP3 file to Downloads: {
                           downloads_mp3_file}")
        time.sleep(SLEEP_DURATION)

    except Exception as e:
        print_with_spacing(f"An error occurred during file move: {e}")


def cleanup(output_path, mp3_file):
    try:
        mp4_file_path = os.path.join(
            output_path, f"{os.path.splitext(os.path.basename(mp3_file))[0]}.mp4")

        if os.path.exists(mp4_file_path):
            os.remove(mp4_file_path)

        rmtree(output_path)

        print_with_spacing("Cleanup done: Removed MP4 and output folder.")
        time.sleep(SLEEP_DURATION)

    except Exception as e:
        print_with_spacing(f"An error occurred during cleanup: {e}")


if __name__ == "__main__":
    while True:
        script_directory = os.path.dirname(sys.executable) if getattr(
            sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(script_directory, "output")

        youtube_url = input(
            "\nEnter the YouTube URL (or press Enter to exit): ")

        if not youtube_url:
            break

        loading_animation()

        video_file = download_video(youtube_url, output_folder)

        if video_file:
            mp3_file = convert_to_mp3(video_file, output_folder)
            if mp3_file:
                move_to_downloads(mp3_file)
                cleanup(output_folder, mp3_file)

    print_with_spacing("Exiting the program.")
