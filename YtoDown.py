import os
import sys
import time
from pytube import YouTube
from shutil import move, rmtree
from moviepy.editor import VideoFileClip
import keyboard
from colorama import Fore, init

SLEEP_DURATION = 2

# Inicjalizacja colorama
init(autoreset=True)


def print_with_spacing(message):
    print(f"\n{message}\n")


def loading_animation():
    for _ in range(6):
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

        print_with_spacing(
            f"{Fore.GREEN}Downloaded video as MP4: {video_file}")
        time.sleep(SLEEP_DURATION)

        return video_file

    except Exception as e:
        print_with_spacing(
            f"{Fore.RED}An error occurred during video download: {e}")
        return None


def convert_to_mp3(video_file, output_path):
    try:
        print_with_spacing(f"{Fore.YELLOW}Converting to MP3...")
        loading_animation()

        mp4_file_renamed = os.path.join(output_path, f"{os.path.splitext(
            os.path.basename(video_file))[0]}_original.mp4")
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
            f"{Fore.RED}An error occurred during MP3 conversion: {e}")
        return None


def move_to_downloads(mp3_file):
    try:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        downloads_mp3_file = os.path.join(
            downloads_path, os.path.basename(mp3_file))
        move(mp3_file, downloads_mp3_file)

        print_with_spacing(f"{Fore.GREEN}Moved MP3 file to Downloads: {
                           downloads_mp3_file}")
        time.sleep(SLEEP_DURATION)

    except Exception as e:
        print_with_spacing(
            f"{Fore.RED}An error occurred during file move: {e}")


def cleanup(output_path, mp3_file):
    try:
        mp4_file_path = os.path.join(output_path, f"{os.path.splitext(
            os.path.basename(mp3_file))[0]}_original.mp4")

        if os.path.exists(mp4_file_path):
            os.remove(mp4_file_path)

        rmtree(output_path)

        print_with_spacing(
            f"{Fore.GREEN}Cleanup done: Removed original MP4 and output folder.")
        time.sleep(SLEEP_DURATION)

    except Exception as e:
        print_with_spacing(f"{Fore.RED}An error occurred during cleanup: {e}")


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
            time.sleep(0.2)  # delay to avoid fast scrolling
        elif keyboard.is_pressed('up'):
            selected_option = (selected_option - 1) % len(options)
            time.sleep(0.2)  # delay to avoid fast scrolling

        if keyboard.is_pressed('enter'):
            return selected_option


if __name__ == "__main__":
    while True:
        script_directory = os.path.dirname(sys.executable) if getattr(
            sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(script_directory, "output")

        youtube_url = input(
            "\nEnter the YouTube URL (or press Enter to exit): ")

        if not youtube_url:
            break

        options = [
            "Download and Convert to MP3",
            "Download Only (MP4)",
            "Skip and Continue",
            "Exit"
        ]

        selected_option = user_choice_menu(options)

        if selected_option == 3:  # Exit
            break
        elif selected_option == 2:  # Skip and Continue
            print_with_spacing(f"{Fore.YELLOW}Skipping and continuing...")
            time.sleep(SLEEP_DURATION)
            continue

        loading_animation()

        video_file = download_video(youtube_url, output_folder)

        if video_file:
            if selected_option == 0:  # Download and Convert to MP3
                mp3_file = convert_to_mp3(video_file, output_folder)
                if mp3_file:
                    move_to_downloads(mp3_file)
                    cleanup(output_folder, mp3_file)
            elif selected_option == 1:  # Download Only (MP4)
                move_to_downloads(video_file)
                cleanup(output_folder, video_file)

    print_with_spacing("Exiting the program.")
