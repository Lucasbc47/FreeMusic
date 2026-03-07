import os
import re
import tkinter.messagebox
from threading import Thread

import customtkinter as ctk
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
    PLAYLIST_URL_PATTERN = (
        r"^(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([\w-]+)(?:\S+)?$"
    )

    def __init__(self):
        # Flag pra evitar múltiplos downloads simultâneos
        self.downloading = False

        self.janela = ctk.CTk()
        self.janela.title("FreeMusic")
        self.janela.geometry("360x175")
        self.janela.configure(fg_color="#599191")
        self.janela.resizable(False, False)

        if os.name == "nt":
            # Verifica se o dispositivo é Windows
            # Linha adicionada para evitar erros
            # ao colocar icone em outros dispositivos.
            self.janela.iconbitmap("imagens/ico.ico")

        url_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        url_frame.pack(pady=(12, 4))

        ctk.CTkLabel(url_frame, text="URL:").pack(side="left", padx=(0, 8))
        self.input_text = ctk.CTkEntry(url_frame, width=250)
        self.input_text.pack(side="left")

        check_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        check_frame.pack(pady=4)

        self.playlist_checkbox = ctk.CTkCheckBox(check_frame, text="Playlist?")
        self.playlist_checkbox.pack(side="left", padx=12)

        self.current_dir_checkbox = ctk.CTkCheckBox(
            check_frame, text="Usar pasta atual"
        )
        self.current_dir_checkbox.pack(side="left", padx=12)

        self.download_button = ctk.CTkButton(
            self.janela,
            text="Instalar",
            command=self.start_download,
            fg_color="black",
            width=160,
        )
        self.download_button.pack(pady=8)

        self.status_label = ctk.CTkLabel(self.janela, text="", text_color="white")
        self.status_label.pack(pady=(0, 6))

    def set_downloading(self, state: bool):
        """Desabilita o botão e mostra status durante o download"""
        self.downloading = state
        self.download_button.configure(state="disabled" if state else "normal")
        self.status_label.configure(text="Baixando..." if state else "")

    def executar(self):
        """
        Roda o programa
        """
        self.janela.mainloop()

    def download(self, url: str, is_playlist: bool, output_path: str):
        """
        Faz o download de um vídeo ou playlist do YouTube como música.

        Argumentos:
            url (str): URL do vídeo ou playlist.
            is_playlist (bool): Define se é uma playlist ou não.
            output_path (str): Caminho da pasta de saída.
        """
        options = {
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
            "format": "bestaudio/best",
            # noplaylist=False permite baixar a playlist inteira de uma vez
            "noplaylist": not is_playlist,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                ydl.download([url])

            title = info.get("title", "Playlist")
            tkinter.messagebox.showinfo("Concluído", f"Download finalizado: {title}")
        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Falha no download:\n{e}")
        finally:
            # Sempre libera o botão, mesmo se der erro
            self.set_downloading(False)

    def start_download(self):
        """
        Thread pra separar processos e evitar que o app fique travado.
        Também valida a URL antes de iniciar.
        """
        if self.downloading:
            return

        url = self.input_text.get().strip()
        is_playlist = self.playlist_checkbox.get()

        if not url:
            tkinter.messagebox.showerror("Erro!", "Favor insira um link do YT!")
            return

        if is_playlist and not re.match(self.PLAYLIST_URL_PATTERN, url):
            tkinter.messagebox.showerror("Erro!", "Este link não é uma playlist!")
            return

        if not is_playlist and not re.match(self.VIDEO_URL_PATTERN, url):
            tkinter.messagebox.showerror("Erro!", "Este link não é um vídeo do YT!")
            return

        if self.current_dir_checkbox.get():
            # Usa a pasta onde o script está localizado
            output_path = os.path.dirname(os.path.abspath(__file__))
        else:
            output_path = ctk.filedialog.askdirectory()
            if not output_path:
                return

        self.set_downloading(True)
        # daemon=True garante que a thread fecha junto com o app
        Thread(
            target=self.download, args=(url, is_playlist, output_path), daemon=True
        ).start()


if __name__ == "__main__":
    # Cria uma instância FreeMusicApp e inicia o app
    # com o metodo executar()
    msc = FreeMusicApp()
    msc.executar()
