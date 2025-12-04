import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

from art import RedNeuronalART1
from utils.procesamiento import cargar_imagen_como_vector

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ArtAppModerno(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RNA")
        self.geometry("1200x650")
        
        self.ancho = 50  
        self.alto = 50
        self.n_entrada = self.ancho * self.alto
        self.max_categorias = 15  
        
        self.red = RedNeuronalART1(self.n_entrada, self.max_categorias, rho=0.8)
        self.vector_actual = None
        self.imagenes_referencia = [] 

      
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_panel_lateral()
        self.crear_area_principal()

    def crear_panel_lateral(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ART ", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

       
        self.btn_cargar = ctk.CTkButton(self.sidebar_frame, text="📂 Cargar Imagen", command=self.cargar_imagen)
        self.btn_cargar.grid(row=1, column=0, padx=20, pady=10)

        self.btn_eliminar = ctk.CTkButton(self.sidebar_frame, text="🗑️ Eliminar Imagen", 
                                          fg_color="#8D4FC3", hover_color="#401555", # Color gris oscuro
                                          command=self.eliminar_imagen_actual)
        self.btn_eliminar.grid(row=2, column=0, padx=20, pady=(0, 10))

        ctk.CTkLabel(self.sidebar_frame, text="Parámetros:", anchor="w").grid(row=3, column=0, padx=20, pady=(20, 0))

        self.lbl_rho = ctk.CTkLabel(self.sidebar_frame, text="Vigilancia (ρ): 0.80")
        self.lbl_rho.grid(row=4, column=0, padx=20, pady=(10, 0))
        
        self.slider_rho = ctk.CTkSlider(self.sidebar_frame, from_=0.0, to=1.0, number_of_steps=20, command=self.actualizar_texto_slider)
        self.slider_rho.set(0.8)
        self.slider_rho.grid(row=5, column=0, padx=20, pady=(0, 20))

        self.btn_procesar = ctk.CTkButton(self.sidebar_frame, text="⚡ APRENDER", fg_color="#2CC985", hover_color="#229A65", text_color="white", font=ctk.CTkFont(weight="bold"), command=self.procesar_aprendizaje)
        self.btn_procesar.grid(row=6, column=0, padx=20, pady=10)

        self.btn_reset = ctk.CTkButton(self.sidebar_frame, text="Reiniciar Red", fg_color="#D84343", hover_color="#A83232", command=self.reiniciar_red)
        self.btn_reset.grid(row=7, column=0, padx=20, pady=(20,10))
        
        self.btn_reset = ctk.CTkButton(self.sidebar_frame, text="Salir", fg_color="#889095", hover_color="#4A4A4A", command=self.salir_red)
        self.btn_reset.grid(row=10, column=0, padx=20, pady=(20,10))


    def crear_area_principal(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
    
        self.frame_entrada = ctk.CTkFrame(self.main_frame)
        self.frame_entrada.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.frame_entrada, text="IMAGEN DE ENTRADA", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.canvas_entrada = ctk.CTkCanvas(self.frame_entrada, width=300, height=300, bg="#1a1a1a", highlightthickness=0)
        self.canvas_entrada.pack(pady=10)
        
        self.lbl_status = ctk.CTkLabel(self.frame_entrada, text="Esperando imagen...", font=ctk.CTkFont(size=16))
        self.lbl_status.pack(pady=10)

        
        self.frame_memoria = ctk.CTkScrollableFrame(self.main_frame, label_text="MEMORIA DE CATEGORÍAS (GALERÍA)", orientation="vertical")
        self.frame_memoria.pack(fill="both", expand=True)

        self.prototipos_canvas = []
        self.botones_eliminar = []
        
        
        columnas_por_fila = 4  
        for i in range(columnas_por_fila):
         
            self.frame_memoria.grid_columnconfigure(i, weight=1)
       
        
        for i in range(self.max_categorias):
            fila_idx = i // columnas_por_fila
            col_idx = i % columnas_por_fila
                    
            
            card = ctk.CTkFrame(self.frame_memoria)
            card.grid(row=fila_idx, column=col_idx, padx=10, pady=10)
                    
       
            ctk.CTkLabel(card, text=f"Cat {i+1}", font=ctk.CTkFont(weight="bold")).pack(pady=(5,0))
                    
           
            c = ctk.CTkCanvas(card, width=120, height=100, bg="#1a1a1a", highlightthickness=0)
            c.pack(padx=10, pady=5)
            self.prototipos_canvas.append(c)
                    
            btn_del = ctk.CTkButton(
                card, 
                text="✕ Eliminar", 
                width=80, 
                height=24,
                fg_color="#D84343", # Rojo
                hover_color="#8B0000", 
                font=ctk.CTkFont(size=11),
                command=lambda index=i: self.eliminar_categoria_especifica(index)
                )
            self.botones_eliminar.append(btn_del)


    def actualizar_texto_slider(self, value):
        self.lbl_rho.configure(text=f"Vigilancia (ρ): {value:.2f}")

    def renderizar_vector(self, canvas, vector, w, h):
        canvas.delete("all")
        matriz = vector.reshape((self.alto, self.ancho))
        
        datos = np.zeros((self.alto, self.ancho, 3), dtype=np.uint8)
        
        datos[matriz == 1] = [0, 255, 255] 
        
        img = Image.fromarray(datos, mode='RGB')
        img = img.resize((w, h), resample=Image.NEAREST)
        img_tk = ImageTk.PhotoImage(img)
        self.imagenes_referencia.append(img_tk)
        
        canvas.create_image(w//2, h//2, image=img_tk)

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.bmp")])
        if not ruta: return
        
        vector = cargar_imagen_como_vector(ruta, self.ancho, self.alto, umbral=150)
        
        if vector is not None:
            self.vector_actual = vector
            self.renderizar_vector(self.canvas_entrada, vector, 300, 300)
            self.lbl_status.configure(text="Imagen cargada.", text_color="white")

    def eliminar_imagen_actual(self):
        self.vector_actual = None
        
        self.canvas_entrada.delete("all")
        
        self.lbl_status.configure(text="Esperando imagen...", text_color="white")

    def procesar_aprendizaje(self):
        if self.vector_actual is None: return
        
        # 1. Actualizar vigilancia desde el slider
        self.red.rho = self.slider_rho.get()
        
        # 2. La red intenta reconocer o aprender
        # Retorna el índice de la categoría (0 a 14) o -1 si falló.
        cat_idx = self.red.aprender_patron(self.vector_actual)
        
        if cat_idx != -1:
            self.lbl_status.configure(text=f"✅ RECONOCIDO: CATEGORÍA {cat_idx + 1}", text_color="#2CC985")
            
            # 3. Actualizar la galería de abajo
            self.actualizar_memoria()
            
            # --- AQUÍ ESTÁ LA MAGIA ---
            # Obtenemos la imagen "limpia" directamente de la memoria de la red
            patron_limpio = self.red.V[cat_idx]
            
            # 4. Reemplazamos visualmente el dibujo del usuario por el patrón limpio
            # Usamos tu función existente renderizar_vector apuntando al canvas de entrada
            self.renderizar_vector(self.canvas_entrada, patron_limpio, 300, 300)
            
            # 5. IMPORTANTE: Actualizamos el vector actual del sistema
            # Para que si el usuario sigue operando, el sistema sepa que ahora la imagen activa es la limpia
            self.vector_actual = patron_limpio
            
        else:
            self.lbl_status.configure(text="⚠️ RED SATURADA O NO RECONOCIDO", text_color="#D84343")
            # -------------------------

    def actualizar_memoria(self):
        # Limpiamos caché de imágenes para no saturar RAM
        self.imagenes_referencia = self.imagenes_referencia[-1:] 
        
        for i in range(self.max_categorias):
            # 1. Verificamos si la neurona está ocupada
            esta_ocupada = self.red.ocupadas[i]
            
            # --- CORRECCIÓN AQUÍ ---
            # Leemos la Matriz V directamente (La memoria real de la red)
            patron = self.red.V[i]
            # -----------------------

            if not esta_ocupada:
                # Si está vacía: Borramos dibujo y ocultamos botón
                self.prototipos_canvas[i].delete("all")
                self.prototipos_canvas[i].create_text(50, 50, text="Vacío", fill="#555", font=("Arial", 10))
                self.botones_eliminar[i].pack_forget() 
            else:
                # Si está llena: Dibujamos el patrón y mostramos botón
                self.renderizar_vector(self.prototipos_canvas[i], patron, 120, 100)
                self.botones_eliminar[i].pack(pady=(0, 10))
           

    def reiniciar_red(self):
        self.red = RedNeuronalART1(self.n_entrada, self.max_categorias, self.slider_rho.get())
        self.vector_actual = None
        self.canvas_entrada.delete("all")
        for c in self.prototipos_canvas: c.delete("all")
        self.lbl_status.configure(text="Memoria reiniciada", text_color="gray")
    
    def salir_red(self):
        self.destroy()
        print("Aplicación cerrada correctamente.")

    def eliminar_categoria_especifica(self, indice):
        self.red.borrar_categoria(indice)
        
        self.actualizar_memoria()
        
        self.lbl_status.configure(text=f"🗑️ Categoría {indice + 1} eliminada.", text_color="orange")

if __name__ == "__main__":
    app = ArtAppModerno()
    app.mainloop()