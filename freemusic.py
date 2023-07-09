import re
import customtkinter as ctk
import tkinter.messagebox
import yt_dlp

class FreeMusic:
    def __init__(self):
        
        ## Propriedades da Janela
        self.janela = ctk.CTk() 
        self.janela.title("FreeMusic")
        self.janela.geometry("344x120")
        self.janela.configure(fg_color="#599191")
        self.janela.resizable(False, False)
        self.janela.wm_iconbitmap = "imagens/ico.ico"
        
        ## Label URL
        self.label_url = ctk.CTkLabel(self.janela, text="URL:")
        self.label_url.grid(row=0, column=0, padx=10, pady=5)

        ## Input URL
        self.input_text = ctk.CTkEntry(self.janela, width=250)
        self.input_text.grid(row=0, column=1, padx=10, pady=5)

        ## Botão Download
        self.download_button = ctk.CTkButton(self.janela, text="Instalar", command=self.on_download_button_click, fg_color="black")
        self.download_button.grid(row=1, column=1, pady=5)

        ## Checkbox Playlist
        self.playlist_checkbox = ctk.CTkCheckBox(self.janela, text="Playlist?")
        self.playlist_checkbox.grid(row=2, column=1, pady=1)

    def executar(self):
        self.janela.mainloop()

    def download(self, video_url: str, playlist: bool, output_path: str):
        """
        Argumentos:
            video_url: string (pode ser video ou playlist)
            playlist: booleano (pode ser true ou false, se é uma playlist.)
            output_path: string (localizacao da pasta saida)
        """
        
        # Configurações do YoutubeDL para música
        as_song_opt = {
            'outtmpl': output_path + '/%(title)s.%(ext)s', 
            # Saida: nome da pasta + titulo + extensão.
            'format': 'bestaudio/best',
            # Melhor formato!
            
            # Processamento
            'postprocessors': [{
                'key': 'FFmpegExtractAudio', # extrair audio com ffmpeg 
                'preferredcodec': 'mp3', # extensão
                'preferredquality': '192', # qualidade
            }],
        }

        # Configurações do YoutubeDL para playlist
        playlist_opt = {
            'extract_flat': True # tratar como lista
        }

        # Instala com YTDL
        with yt_dlp.YoutubeDL(as_song_opt) as ydl:
            if not playlist:
                inf = ydl.extract_info(video_url, download=False)
                ydl.download([video_url])
                tkinter.messagebox.showinfo("Instalação completa!", f"Música instalada: {inf['title']}")


            if playlist:
                def as_playlist(playlist_url: str):
                    with yt_dlp.YoutubeDL(playlist_opt) as ydl_playlist:
                        playlist_info = ydl_playlist.extract_info(playlist_url, download=False)
                        if 'entries' in playlist_info:
                            for entry in playlist_info['entries']:
                                if entry:
                                    video_url = entry['url']
                                    self.download(video_url, playlist=False, output_path=output_path)

                as_playlist(video_url)

    def on_download_button_click(self):

     
        context_url = self.input_text.get()
        is_playlist = self.playlist_checkbox.get()

        # Video URL
        video_url_pattern = r"^(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})(?:\S+)?$"

        # Playlist URL
        playlist_url_pattern = r"^(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([\w-]+)(?:\S+)?$"

        if not context_url:
            tkinter.messagebox.showinfo("Erro!", "Favor insira um link do YT!")
            return
        
        if context_url:
            if is_playlist:
                if not re.findall(playlist_url_pattern, context_url):
                    tkinter.messagebox.showinfo("Erro!", "Este link não é uma playlist!")
                    return
            
            if not is_playlist:
                if not re.findall(video_url_pattern, context_url):
                    tkinter.messagebox.showinfo("Erro!", "Este link não é um vídeo do YT!")
                    return

        output_path = ctk.filedialog.askdirectory()

        if output_path:
            self.download(context_url, is_playlist, output_path)
        
if __name__ == "__main__":
    msc = FreeMusic()
    msc.executar()