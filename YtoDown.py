import os
import sys
import time
from pytube import YouTube
from shutil import move, rmtree
from moviepy.editor import VideoFileClip
import keyboard
from colorama import Fore, init

SLEEP_DURATION = 2

# Colorama initialization
init(autoreset=True)


def clear_screen():
    if os.name == 'nt':
        os.system('cls')


def print_menu(options, selected_option):
    clear_screen()
    print("\nOptions:")
    for i, option in enumerate(options):
        if i == selected_option:
            print(f"{Fore.CYAN} [*] {option}")
        else:
            print(f"{Fore.WHITE} [ ] {option}")


def user_choice_menu(options):
    selected_option = 0

    while True:
        time.sleep(0.1)

        print_menu(options, selected_option)

        if keyboard.is_pressed('down'):
            selected_option = (selected_option + 1) % len(options)
        elif keyboard.is_pressed('up'):
            selected_option = (selected_option - 1) % len(options)

        if keyboard.is_pressed('enter'):
            print(f"{Fore.GREEN}Selected option: {options[selected_option]}")
            return selected_option


def print_with_spacing(message):
    print(f"\n{message}\n")


def loading_animation(processTag=True):
    if processTag:
        for _ in range(6):
            sys.stdout.write("\rProcessing, Please wait.   ")
            time.sleep(0.2)
            sys.stdout.write("\rProcessing, Please wait..  ")
            time.sleep(0.2)
            sys.stdout.write("\rProcessing, Please wait... ")
            time.sleep(0.2)
    else:
        for _ in range(6):
            sys.stdout.write("\rRestarting, Please wait.   ")
            time.sleep(0.2)
            sys.stdout.write("\rRestarting, Please wait..  ")
            time.sleep(0.2)
            sys.stdout.write("\rRestarting, Please wait... ")
            time.sleep(0.2)
    sys.stdout.write("\r")


def download_video_and_convert(url, output_path):
    try:
        youtube = YouTube(url)

        if youtube.age_restricted:
            print_with_spacing(
                "This video is age-restricted. Log in to download.")
            return None

        video_stream = youtube.streams.get_highest_resolution()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        video_title = "".join(c if c.isalnum() or c in [
                              ' ', '.', '-', '_'] else '_' for c in video_stream.title)

        video_file = os.path.join(output_path, f"{video_title}.mp4")
        video_stream.download(output_path, video_file)

        print_with_spacing(f"Downloaded video: {video_file}")
        time.sleep(SLEEP_DURATION)

        mp3_file = convert_to_mp3(video_file, output_path)
        move_to_downloads(mp3_file)
        cleanup(output_path, mp3_file)
        loading_animation(processTag=False)
        clear_screen()
        main()
        clear_screen()

        return video_file

    except Exception as e:
        print_with_spacing(
            f"An error occurred while downloading the video: {e}")
        return None


def convert_to_mp3(video_file, output_path):
    try:
        print_with_spacing(f"{Fore.YELLOW}Converting to MP3...")
        loading_animation(processTag=True)

        mp4_file_renamed = os.path.join(output_path, f"{os.path.splitext(
            os.path.basename(video_file))[0]}.mp4")
        os.rename(video_file, mp4_file_renamed)

        mp3_file = os.path.join(
            output_path, f"{os.path.splitext(mp4_file_renamed)[0]}.mp3")
        clip = VideoFileClip(mp4_file_renamed)
        clip.audio.write_audiofile(mp3_file)
        clip.close()

        print_with_spacing(f"{Fore.GREEN}Converted video to MP3: {mp3_file}")
        time.sleep(SLEEP_DURATION)

        os.remove(mp4_file_renamed)

        return mp3_file

    except Exception as e:
        print_with_spacing(
            f"{Fore.RED}An error occurred while converting to MP3: {e}")
        return None


def move_to_downloads(file_path):
    try:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        downloads_file = os.path.join(
            downloads_path, os.path.basename(file_path))
        move(file_path, downloads_file)

        print_with_spacing(
            f"{Fore.GREEN}Moved file to Downloads: {downloads_file}")
        time.sleep(SLEEP_DURATION)

    except Exception as e:
        print_with_spacing(
            f"{Fore.RED}An error occurred while moving the file: {e}")


def cleanup(output_path, file_path):
    try:
        original_file_path = os.path.join(
            output_path, os.path.basename(file_path))

        if os.path.exists(original_file_path):
            os.remove(original_file_path)

        rmtree(output_path)

        print_with_spacing(
            f"{Fore.GREEN}Cleaned up: Removed original file and output folder.")
        time.sleep(SLEEP_DURATION)

    except Exception as e:
        print_with_spacing(f"{Fore.RED}An error occurred during cleanup: {e}")


def download_video_only(url, output_path):
    try:
        youtube = YouTube(url)

        if youtube.age_restricted:
            print_with_spacing(
                "This video is age-restricted. Log in to download.")
            return None

        video_stream = youtube.streams.get_highest_resolution()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        video_title = "".join(c if c.isalnum() or c in [
                              ' ', '.', '-', '_'] else '_' for c in video_stream.title)

        video_file = os.path.join(output_path, f"{video_title}.mp4")
        video_stream.download(output_path, video_file)

        print_with_spacing(f"Downloaded video: {video_file}")
        time.sleep(SLEEP_DURATION)

        move_to_downloads(video_file)
        cleanup(output_path, video_file)
        loading_animation(processTag=False)
        clear_screen()
        main()
        clear_screen()

    except Exception as e:
        print_with_spacing(
            f"An error occurred while downloading the video: {e}")
        return None


def main():
    script_directory = os.path.dirname(sys.executable) if getattr(
        sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_directory, "output")

    while True:
        youtube_url = input(
            "\nEnter the YouTube video URL (or press Enter to exit): ")

        if not youtube_url:
            print_with_spacing("Closing the program.")
            break

        options = ["Download and convert to MP3", "Download Only MP4"]
        selected_option = user_choice_menu(options)

        if selected_option == 0:
            loading_animation(processTag=True)
            download_video_and_convert(youtube_url, output_folder)

        elif selected_option == 1:
            loading_animation(processTag=True)
            download_video_only(youtube_url, output_folder)


if __name__ == "__main__":
    main()
