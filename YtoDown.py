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
                "To wideo jest ograniczone wiekowo. Zaloguj się, aby pobrać.")
            return None

        video_stream = youtube.streams.get_highest_resolution()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        video_title = "".join(c if c.isalnum() or c in [
                              ' ', '.', '-', '_'] else '_' for c in video_stream.title)

        video_file = os.path.join(output_path, f"{video_title}.mp4")
        video_stream.download(output_path, video_file)

        print_with_spacing(
            f"Pobrano wideo: {video_file}")
        time.sleep(SLEEP_DURATION)

        mp3_file = convert_to_mp3(video_file, output_path)
        if mp3_file:
            move_to_downloads(mp3_file)
            cleanup(output_path, mp3_file)
            clear_screen()
            main()
            clear_screen()

        return video_file

    except Exception as e:
        print_with_spacing(f"Wystąpił błąd podczas pobierania wideo: {e}")
        return None


def convert_to_mp3(video_file, output_path):
    try:
        print_with_spacing(f"{Fore.YELLOW}Konwertowanie do MP3...")
        loading_animation()

        mp4_file_renamed = os.path.join(output_path, f"{os.path.splitext(
            os.path.basename(video_file))[0]}_original.mp4")
        os.rename(video_file, mp4_file_renamed)

        mp3_file = os.path.join(
            output_path, f"{os.path.splitext(mp4_file_renamed)[0]}.mp3")
        clip = VideoFileClip(mp4_file_renamed)
        clip.audio.write_audiofile(mp3_file)
        clip.close()

        print_with_spacing(
            f"{Fore.GREEN}Skonwertowano wideo do MP3: {mp3_file}")
        time.sleep(SLEEP_DURATION)

        os.remove(mp4_file_renamed)

        return mp3_file

    except Exception as e:
        print_with_spacing(
            f"{Fore.RED}Wystąpił błąd podczas konwertowania do MP3: {e}")
        return None


def move_to_downloads(file_path):
    try:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        downloads_file = os.path.join(
            downloads_path, os.path.basename(file_path))
        move(file_path, downloads_file)

        print_with_spacing(
            f"{Fore.GREEN}Przeniesiono plik do folderu Pobrane: {downloads_file}")
        time.sleep(SLEEP_DURATION)

    except Exception as e:
        print_with_spacing(
            f"{Fore.RED}Wystąpił błąd podczas przenoszenia pliku: {e}")


def cleanup(output_path, file_path):
    try:
        original_file_path = os.path.join(
            output_path, os.path.basename(file_path))

        if os.path.exists(original_file_path):
            os.remove(original_file_path)

        rmtree(output_path)

        print_with_spacing(
            f"{Fore.GREEN}Przeczyszczono: Usunięto oryginalny plik i folder wynikowy.")
        time.sleep(SLEEP_DURATION)

    except Exception as e:
        print_with_spacing(
            f"{Fore.RED}Wystąpił błąd podczas czyszczenia: {e}")


def clear_screen():
    if os.name == 'nt':
        os.system('cls')


def print_menu(options, selected_option):
    clear_screen()
    print("\nOpcje:")
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
            print(f"{Fore.GREEN}Wybrana opcja: {options[selected_option]}")
            return selected_option


def main():
    script_directory = os.path.dirname(sys.executable) if getattr(
        sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_directory, "output")

    while True:
        youtube_url = input(
            "\nPodaj URL filmu na YouTube (lub naciśnij Enter, aby zakończyć): ")

        if not youtube_url:
            print_with_spacing("Zamykanie programu.")
            break

        options = ["Pobierz i skonwertuj do MP3", "Zamknij"]
        selected_option = user_choice_menu(options)

        if selected_option == 0:
            download_video(youtube_url, output_folder)

        elif selected_option == 1:
            print_with_spacing("Restartowanie programu...")
            main()


if __name__ == "__main__":
    main()
