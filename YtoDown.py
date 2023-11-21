import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
from shutil import move, rmtree


def download_and_convert_video(url, output_path):
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

        # Convert MP4 to MP3
        mp3_file = os.path.join(output_path, f"{video_stream.title}.mp3")
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(mp3_file)
        clip.close()

        print(f"Converted video to MP3: {mp3_file}")
        return mp3_file

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def move_to_downloads_and_cleanup(mp3_file, output_path):
    try:
        # Move the MP3 file to the user's "Downloads" folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        downloads_mp3_file = os.path.join(
            downloads_path, os.path.basename(mp3_file))
        move(mp3_file, downloads_mp3_file)

        print(f"Moved MP3 file to Downloads: {downloads_mp3_file}")

        # Remove the MP4 file and the output folder
        os.remove(os.path.join(output_path, f"{
                  os.path.splitext(os.path.basename(mp3_file))[0]}.mp4"))
        rmtree(output_path)

        print("Cleanup complete")

    except Exception as e:
        print(f"An error occurred during cleanup: {e}")


if __name__ == "__main__":
    # Get the current folder (the folder where the script is located)
    current_folder = os.path.dirname(__file__)

    youtube_url = input("Enter the YouTube video URL: ")

    # Set the path to the folder where files will be saved
    output_folder = os.path.join(current_folder, "output")

    mp3_file = download_and_convert_video(youtube_url, output_folder)

    if mp3_file:
        move_to_downloads_and_cleanup(mp3_file, output_folder)
