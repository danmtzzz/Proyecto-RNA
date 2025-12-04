import numpy as np

class RedNeuronalART1:
    def __init__(self, num_entrada, num_max_categorias, rho=0.8, gamma=0.5):
        self.N = num_entrada
        self.M = num_max_categorias
        self.rho = rho
        self.gamma = gamma
        
        # Lista para saber qué slots están usados
        self.ocupadas = [False] * self.M
        
        # Matriz V (Memoria/Prototipos - Top Down)
        self.V = np.ones((self.M, self.N))
        
        # Matriz W (Pesos de reconocimiento - Bottom Up)
        val_inicial_w = 1.0 / (1.0 + self.N)
        self.W = np.full((self.M, self.N), val_inicial_w)

    def calcular_activacion(self, entrada):
        return np.dot(self.W, entrada)

    def aprender_patron(self, entrada):
        entrada = np.array(entrada)
        
        #Competencia
        activaciones = self.calcular_activacion(entrada)
        candidatos = np.argsort(activaciones)[::-1]
        
        ganadora_encontrada = False
        indice_ganadora = -1
        
        #Búsqueda en categorías existentes
        for idx in candidatos:
            if not self.ocupadas[idx]:
                continue

            #Recuperar memoria actual
            prototipo_v = self.V[idx]
            
            #Cálculo de similitud (Vigilancia)
            interseccion = np.logical_and(entrada, prototipo_v).astype(int)
            magnitud_interseccion = np.sum(interseccion)
            magnitud_entrada = np.sum(entrada)
            
            rs = 0 if magnitud_entrada == 0 else magnitud_interseccion / magnitud_entrada
            
            if rs >= self.rho:
                # --- RESONANCIA (COINCIDENCIA) ---
                indice_ganadora = idx
                ganadora_encontrada = True
                
                magnitud_memoria = np.sum(prototipo_v)
                
                # Si la ENTRADA tiene MÁS DETALLES (más pixeles) que lo guardado:
                # REEMPLAZAMOS la memoria con esta nueva versión mejorada.
                if magnitud_entrada > magnitud_memoria:
                    # Actualizamos V (Memoria visual)
                    self.V[idx] = entrada
                    
                    # Actualizamos W (Pesos de reconocimiento) acorde a la nueva V
                    nuevo_val_w = 1 / (self.gamma + magnitud_entrada)
                    self.W[idx] = entrada * nuevo_val_w
                    
                
                # Si la entrada tiene MENOS o IGUAL detalles:
                # NO HACEMOS NADA. Nos quedamos con la versión detallada que ya teníamos.
                
                break
        
        #Creación de Nueva Categoría (Si no coincidió con ninguna)
        if not ganadora_encontrada:
            try:
                indice_ganadora = self.ocupadas.index(False)
                
                # Guardamos la entrada como nuevo prototipo
                self.V[indice_ganadora] = entrada
                
                suma_entrada = np.sum(entrada)
                nuevo_val_w = 1 / (self.gamma + suma_entrada)
                self.W[indice_ganadora] = entrada * nuevo_val_w
                
                self.ocupadas[indice_ganadora] = True
                
            except ValueError:
                return -1 # Red llena

        return indice_ganadora

    def borrar_categoria(self, indice):
        if 0 <= indice < self.M:
            self.V[indice] = np.ones(self.N)
            val_inicial_w = 1.0 / (1.0 + self.N)
            self.W[indice] = np.full(self.N, val_inicial_w)
            self.ocupadas[indice] = False