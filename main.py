import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

categorias = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico", ".heic"],
    "Vídeos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp"],
    "Áudio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".mid"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".epub", ".mobi"],
    "Planilhas": [".xls", ".xlsx", ".csv", ".ods"],
    "Apresentações": [".ppt", ".pptx", ".odp", ".key"],
    "Arquivos Compactados": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso"],
    "Código e Scripts": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".go", ".json", ".xml", ".yaml", ".ini"],
    "Executáveis": [".exe", ".msi", ".apk", ".app", ".bat", ".sh", ".deb", ".rpm"],
    "Bases de Dados": [".db", ".sqlite", ".sql", ".mdb"],
    "Fontes": [".ttf", ".otf", ".woff", ".woff2"],
}

def organizar_pasta(caminho, progress_callback):
    if not caminho:
        return 0
    
    os.chdir(caminho)
    arquivos = [f for f in os.listdir() if os.path.isfile(f) and not f.startswith('.')]
    
    total_arquivos = len(arquivos)
    if total_arquivos == 0:
        progress_callback(100)
        return 0
    
    movidos = 0
    for i, arquivo in enumerate(arquivos):
        extensao = os.path.splitext(arquivo)[1].lower()
        if not extensao:
            continue
        
        destino = next((pasta for pasta, exts in categorias.items() if extensao in exts), "Outros")
        
        pasta_destino = os.path.join(caminho, destino)
        os.makedirs(pasta_destino, exist_ok=True)
        
        origem = os.path.join(caminho, arquivo)
        destino_arquivo = os.path.join(pasta_destino, arquivo)
        
        if os.path.exists(destino_arquivo):
            base, ext = os.path.splitext(arquivo)
            contador = 1
            while os.path.exists(destino_arquivo):
                novo_nome = f"{base} ({contador}){ext}"
                destino_arquivo = os.path.join(pasta_destino, novo_nome)
                contador += 1
        
        shutil.move(origem, destino_arquivo)
        movidos += 1
        progress_callback((i + 1) / total_arquivos * 100)
    
    return movidos

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue") 
        
        self.title("Organizador de Pastas")
        self.geometry("500x580")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#0f172a")  
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            main_frame,
            text="Organizador de Pastas",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#e2e8f0"
        ).grid(row=0, column=0, pady=(60, 20))
        
        ctk.CTkLabel(
            main_frame,
            text="Organize seus arquivos por tipo automaticamente",
            font=ctk.CTkFont(size=14),
            text_color="#94a3b8"
        ).grid(row=1, column=0, pady=(0, 50))
        
        self.label_pasta = ctk.CTkLabel(
            main_frame,
            text="Nenhuma pasta selecionada",
            text_color="#64748b",
            font=ctk.CTkFont(size=13),
            wraplength=420,
            justify="center"
        )
        self.label_pasta.grid(row=2, column=0, pady=(0, 30))
        
        self.btn_selecionar = ctk.CTkButton(
            main_frame,
            text="Selecionar Pasta",
            command=self.selecionar_pasta,
            width=300,
            height=50,
            corner_radius=16,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=2,
            border_color="#475569"
        )
        self.btn_selecionar.grid(row=3, column=0, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            width=300,
            height=12,
            corner_radius=8,
            progress_color="#3b82f6",
            fg_color="#1e293b"
        )
        
        self.btn_organizar = ctk.CTkButton(
            main_frame,
            text="Organizar Agora",
            command=self.iniciar_organizacao,
            width=300,
            height=50,
            corner_radius=16,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb"
        )
        self.btn_organizar.grid(row=5, column=0, pady=30)
        
        ctk.CTkLabel(
            main_frame,
            text="por kmdev",
            text_color="#475569",
            font=ctk.CTkFont(size=12, slant="italic")
        ).grid(row=6, column=0, pady=(80, 30))

    def selecionar_pasta(self):
        self.caminho_pasta = filedialog.askdirectory(title="Selecione a pasta para organizar")
        if self.caminho_pasta:
            self.label_pasta.configure(
                text=self.caminho_pasta,
                text_color="#e2e8f0"
            )

    def iniciar_organizacao(self):
        if not hasattr(self, 'caminho_pasta') or not self.caminho_pasta:
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")
            return
        
        self.progress_bar.grid(row=4, column=0, pady=20)
        self.progress_bar.set(0)
        
        self.btn_selecionar.configure(state="disabled")
        self.btn_organizar.configure(state="disabled", text="Organizando...")
        
        def update_progress(value):
            self.progress_bar.set(value / 100)
            self.update_idletasks()
        
        try:
            movidos = organizar_pasta(self.caminho_pasta, update_progress)
            messagebox.showinfo("Concluído!", f"Organização finalizada com sucesso!\n\n{movidos} arquivos movidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a organização:\n\n{str(e)}")
        finally:
            self.progress_bar.grid_forget()
            self.btn_selecionar.configure(state="normal")
            self.btn_organizar.configure(state="normal", text="Organizar Agora")
            self.label_pasta.configure(text="Nenhuma pasta selecionada", text_color="#64748b")
            self.caminho_pasta = None

if __name__ == "__main__":
    app = App()
    app.mainloop()
