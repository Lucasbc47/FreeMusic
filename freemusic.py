import os
import re

from threading import Thread

import customtkinter as ctk
import tkinter.messagebox

import yt_dlp


class FreeMusicApp:
    """
    Aplicação para instalar músicas do Youtube via sua URL.
    Pode escolher entre música individual ou playlist.

    - Autores: 
    Emilaine Briet,
    Letícia Garcia e
    Lucas Costa

    - Feito com youtube-dl e customtkinter
    """
    # Expressões regulares para verificar uma URL de vídeo ou Playlist
    VIDEO_URL_PATTERN = r"^(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})(?:\S+)?$"
    PLAYLIST_URL_PATTERN = r"^(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([\w-]+)(?:\S+)?$"

    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("FreeMusic")
        self.janela.geometry("344x120")
        self.janela.configure(fg_color="#599191")
        self.janela.resizable(False, False)

        if os.name == "nt":
            """
            Verifica se o dispositivo é Windows
            Linha adicionada para evitar erros
            ao colocar icone em outros dispostivos.
            """
            self.janela.iconbitmap("imagens/ico.ico")  

        self.label_url = ctk.CTkLabel(self.janela, text="URL:")
        self.label_url.grid(row=0, column=0, padx=10, pady=5)

        self.input_text = ctk.CTkEntry(self.janela, width=250)
        self.input_text.grid(row=0, column=1, padx=10, pady=5)

        self.download_button = ctk.CTkButton(self.janela, text="Instalar", command=self.threading, fg_color="black")
        self.download_button.grid(row=1, column=1, pady=5)

        self.playlist_checkbox = ctk.CTkCheckBox(self.janela, text="Playlist?")
        self.playlist_checkbox.grid(row=2, column=1, pady=1)

    def threading(self):
        """
        Thread pra separar processos
        E evitar que o app fique crashando
        """
        thread_one = Thread(target=self.on_download_button_click)
        thread_one.start()

    def executar(self):
        """
        Roda o programa
        """
        self.janela.mainloop()

    @staticmethod
    def download(self, video_url: str, playlist: str, output_path: str):
        """
        Faz o download de um vídeo ou playlist do YouTube como música.

        Argumentos:
            video_url (str): URL do vídeo ou playlist.
            playlist (bool): Define se é uma playlist ou não.
            output_path (str): Caminho da pasta de saída.
        """
        # Opções para o YouTubeDL ao baixar como música individual
        song_options = {
            'outtmpl': output_path + '/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }
        # Opções para o YouTubeDL ao baixar uma playlist
        playlist_options = {'extract_flat': True}

        with yt_dlp.YoutubeDL(song_options) as ydl:
            if not playlist:
                info = ydl.extract_info(video_url, download=False)
                ydl.download([video_url])
                tkinter.messagebox.showinfo("Instalação completa!", f"Música instalada: {info['title']}")

            if playlist:
                def download_playlist(playlist_url):
                    with yt_dlp.YoutubeDL(playlist_options) as ydl_playlist:
                        playlist_info = ydl_playlist.extract_info(playlist_url, download=False)
                        if 'entries' in playlist_info:
                            for entry in playlist_info['entries']:
                                if entry:
                                    video_url = entry['url']
                                    self.download(video_url, playlist=False, output_path=output_path)

                download_playlist(video_url)

    def on_download_button_click(self):
        """
        Função chamada após clique no botão download
        """
        context_url = self.input_text.get()
        is_playlist = self.playlist_checkbox.get()

        if not context_url:
            tkinter.messagebox.showinfo("Erro!", "Favor insira um link do YT!")
            return

        if is_playlist and not re.findall(self.PLAYLIST_URL_PATTERN, context_url):
            tkinter.messagebox.showinfo("Erro!", "Este link não é uma playlist!")
            return

        if not is_playlist and not re.findall(self.VIDEO_URL_PATTERN, context_url):
            tkinter.messagebox.showinfo("Erro!", "Este link não é um vídeo do YT!")
            return

        output_path = ctk.filedialog.askdirectory()

        if output_path:
           self.download(context_url, is_playlist, output_path)        


if __name__ == "__main__":
    # Cria uma instância FreeMusicApp e inicia o app
    # com o metodo executar()
    msc = FreeMusicApp()
    msc.executar()
