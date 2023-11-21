import os
from pytube import YouTube


def download_audio_youtube(url, output_path):
    try:
        # Pobierz strumień audio z YouTube
        youtube = YouTube(url)
        audio_stream = youtube.streams.filter(only_audio=True).first()

        # Sprawdź, czy katalog docelowy istnieje, jeśli nie, utwórz go
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Pobierz audio jako plik webm
        mp3_file = os.path.join(output_path, f"{audio_stream.title}.mp3")
        audio_stream.download(output_path, mp3_file)

        print(f"Pobrano audio jako plik MP3: {mp3_file}")
        return mp3_file
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania: {e}")
        return None


if __name__ == "__main__":
    # Pobierz katalog bieżący (folder, w którym znajduje się plik programu)
    current_folder = os.path.dirname(__file__)

    youtube_url = input("Podaj URL do filmu: ")

    # Ustaw ścieżkę do folderu, gdzie mają być zapisane pliki
    output_folder = os.path.join(current_folder, "output")

    mp3_file = download_audio_youtube(youtube_url, output_folder)

    if mp3_file:
        print(f"Plik MP3 dostępny pod ścieżką: {mp3_file}")
