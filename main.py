from util import Util
from youtube_downloader import YoutubeDownloader

def print_menu():
    print("========== PyTube Downloader power by unleed ==========")
    print("Escolha uma opção:")
    print("1. Download de Vídeo (1080p)")
    print("2. Download de Áudio")
    print("3. Download de Playlist")
    print("4. Sair")

def main():
    downloader = YoutubeDownloader()

    while True:
        Util.clear_terminal()
        print_menu()

        choice = input("Opção: ")

        if choice == "1":
            url = input("Insira a URL do vídeo: ")
            downloader.download_video(url)

        elif choice == "2":
            url = input("Insira a URL do vídeo: ")
            downloader.download_audio(url)

        elif choice == "3":
            while True:
                Util.clear_terminal()
                print_menu()

                print("Escolha uma opção para a Playlist:")
                print("1. Download mp4 (video)")
                print("2. Download mp3 (audio only)")
                print("3. Voltar")

                playlist_choice = input("Opção: ")

                if playlist_choice == "1" or playlist_choice == "2":
                    playlist_url = input("Insira a URL da playlist:")
                    downloader.download_playlist(playlist_url, audio_only=playlist_choice == "2")
                elif playlist_choice == "3":
                    break
                else:
                    print("Opção inválida.")

        elif choice == "4":
            break

        else:
            print("Opção inválida. Pressione Enter para continuar.")

if __name__ == "__main__":
    main()
