from util import Util
from youtube_downloader import YoutubeDownloader

def menu():
    while True:
        print("Escolha uma opção:")
        print("1. Download de Vídeo")
        print("2. Download de Áudio")
        print("3. Download de Playlist")
        print("4. Sair")

        choice = input("Opção: ")

        if choice == "1":
            url = input("Insira a URL do vídeo: ")
            downloader.downloadVideo(url)

        elif choice == "2":
            url = input("Insira a URL do vídeo: ")
            downloader.downloadAudio(url)

        elif choice == "3":
            while(True):
                Util.clearTerminal()
                print("Escolha uma opção:")
                print("1. Download mp4 (video)")
                print("2. Download mp3 (audio only)")
                print("3. Back")
                choice = input("Opção: ")
                
                if choice == "1" or choice == "2":
                    url = input("Insira a URL da playlist:")
                    downloader.downloadPlaylist(url, audioOnly=choice == "2")
                elif choice == "3":
                    Util.clearTerminal()
                    break
                else:
                    print("Opção inválida.")
                
        elif choice == "4":
            break

        else:
            Util.clearTerminal()
            print("Opção inválida.")

if __name__ == "__main__":
    downloader = YoutubeDownloader()
    menu()