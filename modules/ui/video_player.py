import customtkinter as ctk
import cv2
import threading
from PIL import Image, ImageTk
import os


class VideoBackgroundPlayer:
    """Reproductor de video de fondo para la interfaz CTk."""
    
    def __init__(self, parent, video_path, width=800, height=600):
        """
        Inicializa el reproductor de video.
        
        Args:
            parent: Frame padre de CTk
            video_path: Ruta del archivo de video
            width: Ancho del canvas de video
            height: Alto del canvas de video
        """
        self.parent = parent
        self.video_path = video_path
        self.width = width
        self.height = height
        self.is_playing = False
        self.cap = None
        self.photo = None
        self.canvas = None
        
        # Crear canvas para mostrar video
        self.canvas = ctk.CTkCanvas(
            parent,
            width=width,
            height=height,
            bg="#131820",
            highlightthickness=0
        )
        
        # Thread para reproducción de video
        self.video_thread = None
        
    def get_canvas(self):
        """Retorna el canvas del video."""
        return self.canvas
    
    def play(self):
        """Inicia la reproducción del video."""
        if not os.path.exists(self.video_path):
            print(f"Video no encontrado: {self.video_path}")
            return False
        
        self.is_playing = True
        self.video_thread = threading.Thread(target=self._play_video, daemon=True)
        self.video_thread.start()
        return True
    
    def stop(self):
        """Detiene la reproducción del video."""
        self.is_playing = False
        if self.cap is not None:
            self.cap.release()
        if self.video_thread is not None:
            self.video_thread.join(timeout=1)
    
    def _play_video(self):
        """Hilo para reproducir el video de forma continua en loop."""
        self.cap = cv2.VideoCapture(self.video_path)
        
        if not self.cap.isOpened():
            print(f"No se pudo abrir el video: {self.video_path}")
            self.is_playing = False
            return
        
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30
        frame_delay = int(1000 / fps)  # Milisegundos
        
        while self.is_playing:
            ret, frame = self.cap.read()
            
            if not ret:
                # Reiniciar el video desde el principio (loop)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
                if not ret:
                    break
            
            # Redimensionar frame al tamaño del canvas
            frame = cv2.resize(frame, (self.width, self.height))
            
            # Convertir BGR a RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convertir a PIL Image
            pil_image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=pil_image)
            
            # Mostrar en canvas
            if self.canvas.winfo_exists():
                self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
                self.canvas.update()
            else:
                break
            
            # Esperar según FPS
            self.parent.after(frame_delay, lambda: None)
        
        self.cap.release()
    
    def set_opacity(self, opacity):
        """
        Establece la opacidad del video (0.0 a 1.0).
        Nota: Esta función requiere soporte de alpha channel en el video.
        """
        pass


class VideoLayer(ctk.CTkFrame):
    """Frame que contiene video de fondo con contenido superpuesto."""
    
    def __init__(self, parent, video_path, content_widget=None, **kwargs):
        """
        Inicializa la capa de video.
        
        Args:
            parent: Frame padre de CTk
            video_path: Ruta del archivo de video
            content_widget: Widget de contenido para superponer sobre el video
        """
        super().__init__(parent, **kwargs)
        self.video_player = None
        self.video_path = video_path
        self.content_widget = content_widget
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Crear reproductor si el video existe
        if os.path.exists(video_path):
            self.video_player = VideoBackgroundPlayer(self, video_path, width=800, height=600)
            video_canvas = self.video_player.get_canvas()
            video_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Superponer contenido si se proporciona
        if content_widget:
            content_widget.grid(row=0, column=0, sticky="nsew")
    
    def play_video(self):
        """Inicia la reproducción del video."""
        if self.video_player:
            self.video_player.play()
    
    def stop_video(self):
        """Detiene la reproducción del video."""
        if self.video_player:
            self.video_player.stop()
