from PIL import Image, ImageEnhance, ImageOps, ImageFilter # <--- IMPORTANTE: Nuevo import
import numpy as np

def cargar_imagen_como_vector(ruta_archivo, ancho=50, alto=50, umbral=128):
    """
    Carga una imagen, ENGROSA las líneas finas artificialmente y luego la procesa
    para que la red ART1 no pierda detalles delgados.
    """
    try:
        #Se convierte la imagen a una escala de grises
        img = Image.open(ruta_archivo).convert('L')
        
        #Engrosamiento de lineas
        img = img.filter(ImageFilter.MinFilter(size=3)) 
        
        #Aumento de Contraste
        realzador = ImageEnhance.Contrast(img)
        img = realzador.enhance(2.0) # Contraste x2
        
        #Reducción 
        img = img.resize((ancho, alto), resample=Image.LANCZOS)
        
        #Binarización
        matriz_img = np.array(img)
        
        #Umbral agresivo: Todo lo que no sea casi blanco, es negro.
        vector_binario = (matriz_img < umbral).astype(int)
        
        return vector_binario.flatten()
        
    except FileNotFoundError:
        print(f"[ERROR] No se encontró la imagen: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"[ERROR] Falló el procesamiento: {e}")
        return None
