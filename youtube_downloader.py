from pytube import YouTube, Playlist
import sys
import os

from util import Util

class YoutubeDownloader:
    def __init__(self):
        self.download_dir = os.path.join("downloaded")
    
    def _progressFunction(self, chunk, file_handle, bytes_remaining):
        global filesize
        current = ((filesize - bytes_remaining)/filesize)
        percent = ('{0:.1f}').format(current*100)
        progress = int(50*current)
        status = '█' * progress + '-' * (50 - progress)
        sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
        sys.stdout.flush()
    
    def _fixFilename(self, filename: str):
        for char in r"\/:*?<>|":
            filename = filename.replace(char, "_")
        return filename
    
    def _checkDownloadDir(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def downloadVideo(self, video_url: str, isPlaylist: bool=False):
        global filesize
        self._checkDownloadDir()
        
        video = YouTube(video_url, on_progress_callback=self._progressFunction)
        
        stream = video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        filesize = stream.filesize
        filename = f"{self._fixFilename(video.title)}.mp4"

        try:
            print(f'Baixando arquivo {filename}...')
            stream.download(filename=filename, output_path=self.download_dir)
            if not isPlaylist: Util.clearTerminal()
            print('Arquivo salvo na pasta downloaded')
        except OSError as e:
            if not isPlaylist: Util.clearTerminal()
            print(f"Erro ao baixar o video: {video.title} - {e}")
            return False

        return True

    def downloadAudio(self, video_url: str, isPlaylist: bool=False):
        global filesize
        self._checkDownloadDir()
        video = YouTube(video_url, on_progress_callback=self._progressFunction)
        
        stream = video.streams.get_audio_only()
        filesize = stream.filesize
        filename = f"{self._fixFilename(video.title)}.mp3"

        try:
            print(f'Baixando arquivo {filename}...')
            stream.download(filename=filename, output_path=self.download_dir)
            if not isPlaylist: Util.clearTerminal()
            print('Arquivo salvo na pasta downloaded')
        except OSError as e:
            if not isPlaylist: Util.clearTerminal()
            print(f"Erro ao baixar o video: {video.title} - {e}")
            return False

        return True

    def downloadPlaylist(self, playlist_url: str, audioOnly: bool=False):
        successful_downloads = 0
        failed_downloads = 0

        # Import Playlist object from pytube
        playlist = Playlist(playlist_url)
        
        if not playlist.title:
            print(f"Playlist indisponível")
            return False

        for video in playlist.videos:
            self._checkDownloadDir()
        
            if audioOnly:
                success = self.downloadAudio(video.embed_url, isPlaylist=True)
            else:
                success = self.downloadVideo(video.embed_url, isPlaylist=True)

            if success:
                successful_downloads += 1
            else:
                failed_downloads += 1
                
        Util.clearTerminal()
        print(f"{successful_downloads} videos baixados com sucesso e {failed_downloads} falhas.")