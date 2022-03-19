
import curses
from curses import wrapper
import numpy as np
import time

global matriz
global margenVertical
global margenHorizontal
matriz = np.zeros((27, 27))

margenVertical = 2
margenHorizontal = 2


def inicializarColoresTerminal():
  curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2,curses.COLOR_BLUE, curses.COLOR_WHITE)
  curses.init_pair(3,curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(4,curses.COLOR_BLUE, curses.COLOR_BLACK)

def inicializarMensajeBienvenida(stdscr):
  stdscr.clear()
  stdscr.addstr(0,0,"TP - 1 / Simulacion & Modelizacion / 2022 - 1C", curses.color_pair(1))
  stdscr.addstr(1,0,"Para salir de programa 'Q', para procesar 'B', para reiniciar proceso 'R', modo automatico 'A'", curses.color_pair(2))
  stdscr.refresh()

def obtenerMatriz(nombreArchivo):
  archivo =  np.loadtxt(nombreArchivo, delimiter=' ')
  return archivo
  
def cargarMatriz(archivo):
  for casilla in archivo:
    matriz[int(casilla[0]) + margenVertical , int(casilla[1]) + margenHorizontal] = 1
  
def mostrarMatriz(screen):
  screen.addstr(3,0,"Matriz cargada en archivo input", curses.color_pair(2))
  despVertical = 5
  despHorizontal = 5
  for fila in range(len(matriz)):
      for columna in range(len(matriz[fila])):
        try:
          if (matriz[fila][columna] == 0):
              screen.addstr(fila + despVertical, columna + despHorizontal, "-", curses.color_pair(4))

          else:
              screen.addstr(fila + despVertical, columna + despHorizontal, 'X', curses.color_pair(3))
        except:
          pass
  screen.refresh()
     
def calcularVecinos(fila, columna, matriz):
    a = matriz[fila-1][columna]  
    b = matriz[fila-1][columna-1]
    c = matriz[fila-1][columna+1]  
    f = matriz[fila+1][columna-1] 
    g = matriz[fila+1][columna] 
    h = matriz[fila+1][columna+1] 
    d = matriz[fila][columna-1]  
    e = matriz[fila][columna+1]    
    return int((a+b+c+d+e+f+g+h))
         
def generarEvolucionIndividual(fila, columna, matriz):
  cantidadAlrededor = calcularVecinos(fila, columna, matriz)
  evolucionReturn = 0
  if matriz[fila][columna] == 1: 
      if cantidadAlrededor < 2: 
          evolucionReturn = 0
      if (cantidadAlrededor == 2 or cantidadAlrededor == 3):
          evolucionReturn = 1
      if cantidadAlrededor > 3:
          evolucionReturn = 0
  else:
    if cantidadAlrededor == 3:
      evolucionReturn = 1
    else:
      evolucionReturn = 0
  return evolucionReturn
              
def generarGeneracion(screen):
  screen.clear()    
  mc = matriz.copy()    
  for fila in range(2, len(matriz)-2):
      for columna in range(2, len(matriz[fila])-2):
          matriz[fila][columna] = generarEvolucionIndividual(fila, columna, mc)
          imprimirCasila(int(matriz[fila][columna]), fila, columna, screen)            
  screen.refresh() 
  
def imprimirCasila(celula, fila, columna, screen):
  despVertical = 5
  despHorizontal = 5
  try:
    if (celula == 0):
        screen.addstr(fila + despVertical, columna + despHorizontal, '- ', curses.color_pair(4))
    else:
        screen.addstr(fila + despVertical, columna + despHorizontal, 'X ', curses.color_pair(3))
  except:
    pass
  
def reiniciarProceso(stdscr):
  stdscr.clear()
  stdscr.refresh()
  global matriz
  matriz = np.zeros((27, 27))
  inicializarMensajeBienvenida(stdscr)
  archivoPlano = obtenerMatriz('./input.txt')
  cargarMatriz(archivoPlano)
  mostrarMatriz(stdscr)
  
def comenzarProceso(stdscr, cicloVida):
  generarGeneracion(stdscr)
  try:
    stdscr.addstr(35,5, '"Q" para salir de programa')    
    stdscr.addstr(36,5, '"R" para volver atras')    
    stdscr.addstr(33,5, 'Cantidad de ciclos: {}'.format(cicloVida)) 
    stdscr.refresh()   
  except:
    pass

def main(stdscr):
  inicializarColoresTerminal()
  inicializarMensajeBienvenida(stdscr)
  inicializarProceso = False
  archivoPlano = obtenerMatriz('./input.txt')
  cargarMatriz(archivoPlano)
  mostrarMatriz(stdscr)
  teclaIngreso = stdscr.getch()
  cicloVida = 1
  ciclosMaximos = 200
  while teclaIngreso != ord('q'):
    if(teclaIngreso == ord('b') or inicializarProceso):
      comenzarProceso(stdscr, cicloVida)
      inicializarProceso = True
      cicloVida += 1 
    if(teclaIngreso == ord('r') and inicializarProceso):
      reiniciarProceso(stdscr);
      inicializarProceso = False
      cicloVida = 1
    if(teclaIngreso == ord('a')):
      reiniciarProceso(stdscr)
      cicloVida = 1
      while(cicloVida <= ciclosMaximos):
        comenzarProceso(stdscr, cicloVida)
        time.sleep(0.2)
        cicloVida+=1
 
    teclaIngreso = stdscr.getch()



#Inicializacion de Consola StdScr Output
wrapper(main)