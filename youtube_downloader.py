from pytube import YouTube, Playlist
import sys
import os

from util import Util

class YoutubeDownloader:
    def __init__(self):
        self.download_dir = "downloaded"
        self._check_download_dir()

    def _progress_callback(self, chunk, file_handle, bytes_remaining):
        global filesize
        current = (filesize - bytes_remaining) / filesize
        percent = f'{current*100:.1f}'
        progress = int(50 * current)
        status = '█' * progress + '-' * (50 - progress)
        sys.stdout.write(f' ↳ |{status}| {percent}%\r')
        sys.stdout.flush()

    def _fix_filename(self, filename: str):
        invalid_chars = r"\/:*?<>|"
        return ''.join('_' if char in invalid_chars else char for char in filename)

    def _check_download_dir(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def get_filesize(self, stream):
        # Tenta obter o tamanho do arquivo da stream; se não for possível, retorna 0
        try:
            return int(stream.filesize)
        except (AttributeError, TypeError):
            return 0

    def download_video(self, video_url: str):
        global filesize
        self._check_download_dir()

        video = YouTube(video_url, on_progress_callback=self._progress_callback)

        # Obtém todas as streams de vídeo disponíveis / mude para mkv se achar melhor
        video_streams = video.streams.filter(file_extension='mp4', only_video=True)

        # Escolhe a stream de maior resolução de acordo com o link do video
        stream = video_streams.order_by('resolution').desc().first()

        if stream is None:
            print("Erro: Não foi possível obter a stream para a resolução mais alta.")
            return False

        filesize = self.get_filesize(stream)
        filename = f"{self._fix_filename(video.title)}.mp4"

        try:
            print(f'Baixando arquivo {filename}...')
            stream.download(filename=filename, output_path=self.download_dir)
            Util.clear_terminal()
            print('Arquivo salvo na pasta downloaded')
        except OSError as e:
            Util.clear_terminal()
            print(f"Erro ao baixar o vídeo: {video.title} - {e}")
            return False

        return True

    def download_audio(self, video_url: str):
        global filesize
        self._check_download_dir()
        video = YouTube(video_url, on_progress_callback=self._progress_callback)
        
        stream = video.streams.get_audio_only()
        filesize = self.get_filesize(stream)
        filename = f"{self._fix_filename(video.title)}.mp3"

        try:
            print(f'Baixando arquivo {filename}...')
            stream.download(filename=filename, output_path=self.download_dir)
            Util.clear_terminal()
            print('Arquivo salvo na pasta downloaded')
        except OSError as e:
            Util.clear_terminal()
            print(f"Erro ao baixar o vídeo: {video.title} - {e}")
            return False

        return True

    def download_playlist(self, playlist_url: str, audio_only: bool = False):
        successful_downloads = 0
        failed_downloads = 0

        playlist = Playlist(playlist_url)

        if not playlist.title:
            print("Playlist indisponível")
            return False

        for video in playlist.videos:
            self._check_download_dir()

            if audio_only:
                success = self.download_audio(video.embed_url)
            else:
                success = self.download_video(video.embed_url)

            if success:
                successful_downloads += 1
            else:
                failed_downloads += 1

        Util.clear_terminal()
        print(f"{successful_downloads} vídeos baixados com sucesso e {failed_downloads} falhas.")
