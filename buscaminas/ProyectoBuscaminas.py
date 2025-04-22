import pygame 
import random
 
 # Inicializar Pygame
pygame.init()
 
 # Definir colores
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
ROSA = (0, 0, 0)
AMARILLO = (255, 0, 0)
CELESTE = (0, 0, 255)
MARRON = (0, 128, 0)
 
 # Definir dimensiones del juego
ANCHO_CELDA = 30
MARGEN = 2
FILAS = 15
COLUMNAS = 15
NUM_MINAS = 20
ANCHO_PANTALLA = (ANCHO_CELDA + MARGEN) * COLUMNAS + MARGEN
ALTO_PANTALLA = (ANCHO_CELDA + MARGEN) * FILAS + MARGEN + 50  # Espacio para el estado

# Rango maximo derevelacion de contenido en casillas
RANGO_MAXIMO = 5
 
 # Crear la ventana
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Buscaminas Sencillo")
 
 # Cargar fuente
fuente = pygame.font.Font(None, 30)
fuente_pequena = pygame.font.Font(None, 20)
 
 # Estructura del juego
cuadricula = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]  # 0: vacía, -1: mina
revelado = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]
marcado = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]
game_over = False
primera_jugada = True
 
 # Funciones
 
def generar_minas():
   minas_colocadas = 0
   while minas_colocadas < NUM_MINAS:
       fila = random.randint(0, FILAS - 1)
       columna = random.randint(0, COLUMNAS - 1)
       if cuadricula[fila][columna] == 0:
             cuadricula[fila][columna] = -1
             minas_colocadas += 1
 
def calcular_adyacentes():
     for fila in range(FILAS):
         for columna in range(COLUMNAS):
             if cuadricula[fila][columna] != -1:
                 minas_adyacentes = 0
                 for i in range(max(0, fila - 1), min(FILAS, fila + 2)):
                     for j in range(max(0, columna - 1), min(COLUMNAS, columna + 2)):
                         if cuadricula[i][j] == -1:
                             minas_adyacentes += 1
                 cuadricula[fila][columna] = minas_adyacentes
 
def dibujar_cuadricula():
     for fila in range(FILAS):
         for columna in range(COLUMNAS):
             color = GRIS
             if revelado[fila][columna]:
                 color = BLANCO
             pygame.draw.rect(pantalla, color,
                              [(MARGEN + ANCHO_CELDA) * columna + MARGEN,
                               (MARGEN + ANCHO_CELDA) * fila + MARGEN,
                               ANCHO_CELDA, ANCHO_CELDA])
             if marcado[fila][columna]:
                 pygame.draw.rect(pantalla, AMARILLO,
                                  [(MARGEN + ANCHO_CELDA) * columna + MARGEN + 5,
                                   (MARGEN + ANCHO_CELDA) * fila + MARGEN + 5,
                                   ANCHO_CELDA - 10, ANCHO_CELDA - 10])
             elif revelado[fila][columna]:
                 if cuadricula[fila][columna] == -1:
                     pygame.draw.circle(pantalla, ROSA,
                                        [(MARGEN + ANCHO_CELDA) * columna + MARGEN + ANCHO_CELDA // 2,
                                         (MARGEN + ANCHO_CELDA) * fila + MARGEN + ANCHO_CELDA // 2],
                                        ANCHO_CELDA // 3)
                 elif cuadricula[fila][columna] > 0:
                     texto = fuente.render(str(cuadricula[fila][columna]), True, CELESTE if cuadricula[fila][columna] < 3 else MARRON if cuadricula[fila][columna] < 5 else AMARILLO)
                     texto_rect = texto.get_rect(center=((MARGEN + ANCHO_CELDA) * columna + MARGEN + ANCHO_CELDA // 2,
                                                        (MARGEN + ANCHO_CELDA) * fila + MARGEN + ANCHO_CELDA // 2))
                     pantalla.blit(texto, texto_rect)
 
def revelar_celda(fila, columna):
     if 0 <= fila < FILAS and 0 <= columna < COLUMNAS and not revelado[fila][columna] and not marcado[fila][columna]:
         revelado[fila][columna] = True
         if cuadricula[fila][columna] == 0:
             for i in range(max(0, fila - 1), min(FILAS, fila + 2)):
                 for j in range(max(0, columna - 1), min(COLUMNAS, columna + 2)):
                     revelar_celda(i, j)
         elif cuadricula[fila][columna] == -1:
             global game_over
             game_over = True
             for r in range(FILAS):
                 for c in range(COLUMNAS):
                     if cuadricula[r][c] == -1:
                         revelado[r][c] = True
 
def marcar_celda(fila, columna):
     if not revelado[fila][columna]:
         marcado[fila][columna] = not marcado[fila][columna]
 
def verificar_ganador():
     for fila in range(FILAS):
         for columna in range(COLUMNAS):
             if cuadricula[fila][columna] != -1 and not revelado[fila][columna]:
                 return False
     return True
 
 # Bucle principal del juego
ejecutando = True
while ejecutando:
     for evento in pygame.event.get():
         if evento.type == pygame.QUIT:
             ejecutando = False
         elif evento.type == pygame.MOUSEBUTTONDOWN:
             pos = pygame.mouse.get_pos()
             columna = pos[0] // (ANCHO_CELDA + MARGEN)
             fila = pos[1] // (ANCHO_CELDA + MARGEN)
 
             if fila < FILAS and columna < COLUMNAS:
                 if evento.button == 1:  # Clic izquierdo
                     if primera_jugada:
                         generar_minas()
                         calcular_adyacentes()
                         primera_jugada = False
                     def revelar_celda(fila, columna, rango_actual=RANGO_MAXIMO):
                      global game_over
                     if 0 <= fila < FILAS and 0 <= columna < COLUMNAS and not revelado[fila][columna] and not marcado[fila][columna] and rango_actual > 0:
                      revelado[fila][columna] = True
                      if cuadricula[fila][columna] == 0:
                       for i in range(max(0, fila - 1), min(FILAS, fila + 2)):
                         for j in range(max(0, columna - 1), min(COLUMNAS, columna + 2)):
                          # Llamamos recursivamente a revelar_celda, decrementando el rango
                          revelar_celda(i, j, rango_actual - 1) 
                     elif cuadricula[fila][columna] == -1:
            
                       game_over = True 
                       for r in range(FILAS):
                        for c in range(COLUMNAS):
                          if cuadricula[r][c] == -1:
                           revelado[r][c] = True
                          elif evento.button == 1:  # Clic izquierdo
                            if primera_jugada:
                             generar_minas()
                             calcular_adyacentes()
                             primera_jugada = False
                     revelar_celda(fila, columna, 5) # Puedes ajustar el rango máximo aquí
                 elif evento.button == 3:  # Clic derecho
                     marcar_celda(fila, columna)
 
     # Dibujar la pantalla
     pantalla.fill(ROSA)
     dibujar_cuadricula()
 
     # Mostrar estado del juego
     mensaje = ""
     color_mensaje = BLANCO
     if game_over:
         mensaje = "¡BOOM! Perdiste, Suerte la Proxima :) ."
         color_mensaje = AMARILLO
     elif verificar_ganador():
         mensaje = "¡Ganaste Felicidades!"
         color_mensaje = MARRON
 
     texto_estado = fuente.render(mensaje, True, color_mensaje)
     texto_rect_estado = texto_estado.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 25))
     pantalla.blit(texto_estado, texto_rect_estado)
 
     # Actualizar la pantalla
     pygame.display.flip()
 
 # Salir de Pygame
pygame.quit() 