#Juego concéntrese.

#Samuelle Portela & Angie Michelle Gonzalez.

class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False
        """
        Una cosa es la fuente de la imagen (es decir, el nombre del archivo) y otra
        la imagen lista para ser pintada por PyGame
        La fuente la necesitamos para más tarde, comparar las tarjetas
        """
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)


cuadros = [
    [Cuadro("assets/coco.png"), Cuadro("assets/coco.png"),
     Cuadro("assets/manzana.png"), Cuadro("assets/manzana.png")],
    [Cuadro("assets/limón.png"), Cuadro("assets/limón.png"),
     Cuadro("assets/naranja.png"), Cuadro("assets/naranja.png")],
    [Cuadro("assets/pera.png"), Cuadro("assets/pera.png"),
     Cuadro("assets/piña.png"), Cuadro("assets/piña.png")],
    [Cuadro("assets/plátano.png"), Cuadro("assets/plátano.png"),
     Cuadro("assets/sandía.png"), Cuadro("assets/sandía.png")],
]

# Colores
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (30, 136, 229)

# Los sonidos
sonido_fondo = pygame.mixer.Sound("assets/fondo.wav")
sonido_clic = pygame.mixer.Sound("assets/clic.wav")
sonido_éxito = pygame.mixer.Sound("assets/ganador.wav")
sonido_fracaso = pygame.mixer.Sound("assets/equivocado.wav")
sonido_voltear = pygame.mixer.Sound("assets/voltear.wav")

# La fuente que estará sobre el botón
tamaño_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((anchura_boton / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - altura_boton)

# El botón, que al final es un rectángulo
botón = pygame.Rect(0, altura_pantalla - altura_boton,
                    anchura_boton, altura_pantalla)

# También dibujamos el botón
if juego_iniciado:
    # Si está iniciado, entonces botón blanco con fuente gris para que parezca deshabilitado
    pygame.draw.rect(pantalla_juego, color_blanco, boton)
    pantalla_juego.blit(fuente.render(
        "Iniciar juego", True, color_gris), (xFuente, yFuente))
else:
    pygame.draw.rect(pantalla_juego, color_azul, boton)
    pantalla_juego.blit(fuente.render(
        "Iniciar juego", True, color_blanco), (xFuente, yFuente))


# Ocultar todos los cuadros
def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False


def aleatorizar_cuadros():
    # Elegir X e Y aleatorios, intercambiar
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal


def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(sonido_exito)
        reiniciar_juego()


# Regresa False si al menos un cuadro NO está descubierto. True en caso de que absolutamente todos estén descubiertos
def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True


def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False


def iniciar_juego():
    pygame.mixer.Sound.play(sonido_clic)
    global juego_iniciado
    # Aleatorizar 3 veces
    for i in range(3):
        aleatorizar_cuadros()
    ocultar_todos_los_cuadros()
    juego_iniciado = True


# Si quitan el juego, salimos
if event.type == pygame.QUIT:
    sys.exit()

# Si hicieron clic y el usuario puede jugar...
elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:

    """
    xAbsoluto e yAbsoluto son las coordenadas de la pantalla en donde se hizo
    clic. PyGame no ofrece detección de clic en imagen, por ejemplo. Así que
    se deben hacer ciertos trucos
    """
    # Si el clic fue sobre el botón y el juego no se ha iniciado, entonces iniciamos el juego
    xAbsoluto, yAbsoluto = event.pos
    if boton.collidepoint(event.pos):
        if not juego_iniciado:
            iniciar_juego()

# Si no hay juego iniciado, ignoramos el clic
if not juego_iniciado:
    continue

x = math.floor(xAbsoluto / medida_cuadro)
y = math.floor(yAbsoluto / medida_cuadro)
# Primero lo primero. Si  ya está mostrada o descubierta, no hacemos nada
cuadro = cuadros[y][x]
if cuadro.mostrar or cuadro.descubierto:
    # continue ignora lo de abajo y deja que el ciclo siga
    continue
# Si es la primera vez que tocan la imagen (es decir, no están buscando el par de otra, sino apenas
# están descubriendo la primera)
if x1 is None and y1 is None:
    # Entonces la actual es en la que acaban de dar clic, la mostramos
    x1 = x
    y1 = y
    cuadros[y1][x1].mostrar = True
    pygame.mixer.Sound.play(sonido_voltear)
else:
    # En caso de que ya hubiera una cliqueada anteriormente y estemos buscando el par, comparamos...
    x2 = x
    y2 = y
    cuadros[y2][x2].mostrar = True
    cuadro1 = cuadros[y1][x1]
    cuadro2 = cuadros[y2][x2]
    # Si coinciden, entonces a ambas las ponemos en descubiertas:
    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
        cuadros[y1][x1].descubierto = True
        cuadros[y2][x2].descubierto = True
        x1 = None
        x2 = None
        y1 = None
        y2 = None
        pygame.mixer.Sound.play(sonido_clic)
    else:
        pygame.mixer.Sound.play(sonido_fracaso)
        # Si no coinciden, tenemos que ocultarlas en el plazo de [segundos_mostrar_pieza] segundo(s). Así que establecemos
        # la bandera. Como esto es un ciclo infinito y asíncrono, podemos usar el tiempo para saber
        # cuándo fue el tiempo en el que se empezó a ocultar
        ultimos_segundos = int(time.time())
        # Hasta que el tiempo se cumpla, el usuario no puede jugar
        puede_jugar = False
comprobar_si_gana()

ahora = int(time.time())
# Y aquí usamos la bandera del tiempo, de nuevo. Si los segundos actuales menos los segundos
# en los que se empezó el ocultamiento son mayores a los segundos en los que se muestra la pieza, entonces
# se ocultan las dos tarjetas y se reinician las banderas
if ultimos_segundos is not None and ahora - ultimos_segundos >= segundos_mostrar_pieza:
    cuadros[y1][x1].mostrar = False
    cuadros[y2][x2].mostrar = False
    x1 = None
    y1 = None
    x2 = None
    y2 = None
    últimos_segundos = None
    # En este momento el usuario ya puede hacer clic de nuevo pues las imágenes ya estarán ocultas
    puede_jugar = True

# Hacer toda la pantalla blanca
pantalla_juego.fill(color_blanco)
# Banderas para saber en dónde dibujar las imágenes, pues al final
# la pantalla de PyGame son solo un montón de pixeles
x = 0
y = 0
# Recorrer los cuadros
for fila in cuadros:
    x = 0
    for cuadro in fila:
        """
        Si está descubierto o se debe mostrar, dibujamos la imagen real. Si no,
        dibujamos la imagen oculta
        """
        if cuadro.descubierto or cuadro.mostrar:
            pantalla_juego.blit(cuadro.imagen_real, (x, y))
        else:
            pantalla_juego.blit(imagen_oculta, (x, y))
        x += medida_cuadro
    y += medida_cuadro

# También dibujamos el botón
if juego_iniciado:
    # Si está iniciado, entonces botón blanco con fuente gris para que parezca deshabilitado
    pygame.draw.rect(pantalla_juego, color_blanco, boton)
    pantalla_juego.blit(fuente.render(
        "Iniciar juego", True, color_gris), (xFuente, yFuente))
else:
    pygame.draw.rect(pantalla_juego, color_azul, boton)
    pantalla_juego.blit(fuente.render(
        "Iniciar juego", True, color_blanco), (xFuente, yFuente))

# Actualizamos la pantalla
pygame.display.update()




#líneas de código tomadas https://parzibyte.me/blog/2020/12/05/juego-memorama-memoria-python-pygame/
#para poder ejecutar el código es obligatorio instalar Python y Pip, instalar la dependencia de PyGame y ejecutar el script de memoria.py con:
#pythonmemoria.py 