import pygame, random, math, time, sys
from clases import Vehiculo, Obstaculo, Boton, Aceite
from constantes import *
from base_de_datos import crear_tablas_db, insertar_jugador, obtener_ranking

#INFORMACION DEL JUEGO
PANTALLA = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption(TITULO_VENTANA)

def centrar(imagen):
    """
    Se encarga de centrar en la pantalla.

    Parámetros:
        imagen: la imagen o superficie a centrar.
    
    Retorna:
        la coordena X para centrar la imagen.
    """
    return (ANCHO // 2) - imagen.get_width() // 2

#FONDOS
fondo = pygame.image.load(UBICACION_FONDO).convert()
fondo = pygame.transform.smoothscale(fondo, (ANCHO, ALTURA))
fondo_pista = pygame.image.load(UBICACION_FONDO_PISTA)
fondo_pista = pygame.transform.smoothscale(fondo_pista, (ANCHO, ALTURA))
fondo_opciones = pygame.image.load(UBICACION_FONDO_OPCIONES)
fondo_opciones = pygame.transform.smoothscale(fondo_opciones, (ANCHO, ALTURA))
fondo_ranking = pygame.image.load(UBICACION_FONDO_RANKING)
fondo_ranking = pygame.transform.smoothscale(fondo_ranking, (ANCHO, ALTURA))
fondo_perdiste = pygame.image.load(UBICACION_FONDO_PERDISTE)
fondo_perdiste = pygame.transform.smoothscale(fondo_perdiste, (ANCHO, ALTURA))
fondo_modo_seleccion_auto = pygame.image.load(UBICACION_FONDO_SELECCION_AUTO).convert()
fondo_modo_seleccion_auto = pygame.transform.smoothscale(fondo_modo_seleccion_auto, (ANCHO, ALTURA))

# Imagenes de las Flechas seleccion de auto
flecha_izquierda_imagen = pygame.image.load(UBICACION_BOTON_FLECHA)
flecha_derecha_imagen = pygame.transform.flip(flecha_izquierda_imagen, True, False)

# Imagenes de botones
jugar_imagen = pygame.image.load(UBICACION_BOTON_JUGAR)
pausar_imagen = pygame.image.load(UBICACION_BOTON_PAUSA)
ranking_imagen = pygame.image.load(UBICACION_BOTON_RANKING)
salir_imagen = pygame.image.load(UBICACION_BOTON_SALIR)
volver_imagen = pygame.image.load(UBICACION_BOTON_VOLVER)
guardar_imagen = pygame.image.load(UBICACION_BOTON_GUARDAR)

# Creación de botones
flecha_izquierda_boton = Boton(flecha_izquierda_imagen, (32, 42), 40, 250)
flecha_derecha_boton = Boton(flecha_derecha_imagen, (32, 42), ANCHO-60, 250)
jugar_boton = Boton(jugar_imagen, (140, 50), 120, ALTURA-80)
pausar_boton = Boton(pausar_imagen, (120, 40), centrar(jugar_imagen)+10, ALTURA-50)
volver_boton = Boton(jugar_imagen, (100, 34), 780, ALTURA-80)
jugar_boton_centrado = Boton(jugar_imagen, (100, 34), centrar(jugar_imagen)+10, ALTURA-220)
jugar_boton_centrado_menu = Boton(jugar_imagen, (100, 34), centrar(jugar_imagen)+10, ALTURA-220)

jugar_boton_centrado_inicio = Boton(jugar_imagen, (160, 60), 400, ALTURA-275)
ranking_boton_inicio = Boton(ranking_imagen, (140, 50), 180, ALTURA-270)
salir_boton_inicio = Boton(salir_imagen, (140, 50), 640, ALTURA-270)
jugar_boton_centrado_seleccion_auto = Boton(jugar_imagen, (160, 60), 420, ALTURA-180)

volver_boton_centrado_opciones = Boton(volver_imagen, (150, 50), 310, ALTURA-220)
salir_boton_opciones = Boton(salir_imagen, (150, 50), 550, ALTURA-220)

jugar_boton_centrado_ranking = Boton(jugar_imagen, (150, 50), 310, ALTURA-180)
volver_boton_ranking = Boton(volver_imagen, (150, 50), 550, ALTURA-180)

guardar_boton_perdiste = Boton(guardar_imagen, (150, 50), 310, ALTURA-220)
salir_boton_perdiste = Boton(salir_imagen, (150, 50), 550, ALTURA-220)

# imagenes de los autos a seleccionar
autos = [
    pygame.image.load(UBICACION_AUTO_1),
    pygame.image.load(UBICACION_AUTO_2),
    pygame.image.load(UBICACION_AUTO_3),
    pygame.image.load(UBICACION_AUTO_4),
    pygame.image.load(UBICACION_AUTO_5),
    pygame.image.load(UBICACION_AUTO_6),    
]
tipo_auto = 0

# Funciones
def iniciar_juego(volumen=0.2):
    """
    Inicializa el juego mostrando el menu de opciones.

    Parámetros:
        volumen: el volumen del juego el cual ya viene por defecto inicializado en 0.2 en caso que no se le envie ninguno.
    
    Retorna:
        Nada.
    """
    modo_intro = True
    crear_tablas_db()
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)
    audio_jugar = pygame.mixer.Sound(UBICACION_SONIDO_INICIAR)
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(volumen)

    while modo_intro:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_intro = False
                    seleccion_auto()
                if evento.key == pygame.K_SPACE:
                    audio_jugar.play()
                    modo_intro = False
                    seleccion_auto()
        PANTALLA.blit(fondo, (0, 0))

        if jugar_boton_centrado_inicio.renderizar(PANTALLA):
            audio_jugar.play()
            modo_intro = False
            seleccion_auto()
        if ranking_boton_inicio.renderizar(PANTALLA):
            audio_click.play()
            modo_intro = False
            ranking()
        if salir_boton_inicio.renderizar(PANTALLA):
            audio_click.play()
            modo_intro = False
            sys.exit()
        pygame.display.update()

def mover_flecha(audio, tipo_auto, autos, direccion):
    """
    Funcionalidad al apretar click en la flecha.

    Parámetros:
        audio: el sonido a reproducirse cuando aprete click en alguna de las flechas.
        tipo_auto: el tipo de auto seleccionado.
        autos: los autos disponibles.
        direccion: la dirección de la flecha.
    
    Retorna:
        tipo_auto: el tipo de auto seleccionado.
    """
    if direccion == "derecha":
        tipo_auto += 1
        if tipo_auto >= len(autos):
            tipo_auto = 0
    elif direccion == "izquierda":
        tipo_auto -= 1
        if tipo_auto < 0:
            tipo_auto = len(autos) - 1
    audio.play()
    return tipo_auto

def iniciar_bucle_juego(tipo_auto, volumen):
    """
    Inicia la carrera de autos.

    Parámetros:
        volumen: el volumen de la musica del juego.
        tipo_auto: el tipo de auto seleccionado.
    
    Retorna:
        False.
    """
    bucle_de_juego("imagenes/autos/auto{0}.png".format(tipo_auto + 1), volumen)
    return False

def seleccion_auto(volumen=0.2):
    """
    El menu de autos disponibles para seleccionar en la carrera.

    Parámetros:
        volumen: el volumen del juego el cual ya viene por defecto inicializado en 0.2 en caso que no se le envie ninguno.
    
    Retorna:
        Nada.
    """
    modo_seleccion_auto = True
    tipo_auto = 0
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)
    audio_jugar = pygame.mixer.Sound(UBICACION_SONIDO_INICIAR)

    while modo_seleccion_auto:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_seleccion_auto = False
                if evento.key == pygame.K_RIGHT:
                    tipo_auto = mover_flecha(audio_click, tipo_auto, autos, "derecha")
                if evento.key == pygame.K_LEFT:
                    tipo_auto = mover_flecha(audio_click, tipo_auto, autos, "izquierda")
                if evento.key == pygame.K_SPACE:
                    audio_jugar.play()
                    modo_seleccion_auto = iniciar_bucle_juego(tipo_auto, volumen)
                    
        PANTALLA.blit(fondo_modo_seleccion_auto, (0, 0))

        auto_actual = autos[tipo_auto]
        posicion_x = (ANCHO - auto_actual.get_width()) // 2  # Calcula la posición x centrada
        PANTALLA.blit(auto_actual, (posicion_x, 150))
        
        if flecha_izquierda_boton.renderizar(PANTALLA):
            tipo_auto = mover_flecha(audio_click, tipo_auto, autos, "izquierda")

        if flecha_derecha_boton.renderizar(PANTALLA):
            tipo_auto = mover_flecha(audio_click, tipo_auto, autos, "derecha")

        if jugar_boton_centrado_seleccion_auto.renderizar(PANTALLA):
            audio_jugar.play()
            modo_seleccion_auto = iniciar_bucle_juego(tipo_auto, volumen)

        pygame.display.flip()

def mostrar_resultados(PANTALLA, autos_pasados, puntuacion, nivel, tiempo):
    """
    Muestra los resultados de la carrera.

    Parámetros:
        PANTALLA: el objeto de pantalla para poder mostrar objetos
        autos_pasados: la cantidad de autos pasados durante la carrera
        puntuacion: la cantidad de puntos conseguidos
        nivel: el nivel de la carrera
        tiempo: el tiempo transcurrido desde que inicio la carrera
    
    Retorna:
        Nada.
    """
    fuente = pygame.font.SysFont("Arial", 24)
    autos_pasados_texto = fuente.render("Autos pasados: " + str(autos_pasados), True, AMARILLO)
    puntuacion_texto = fuente.render("Puntuacion: " + str(puntuacion), True, AMARILLO)
    nivel_texto = fuente.render("Nivel: " + str(nivel), True, AMARILLO)
    tiempo_texto = fuente.render("Tiempo: " + str(tiempo//1000) + " segundos", True, AMARILLO)
    PANTALLA.blit(autos_pasados_texto, (10,ALTURA - 70))
    PANTALLA.blit(puntuacion_texto, (10,ALTURA - 45))
    PANTALLA.blit(nivel_texto, (700, ALTURA - 70))
    PANTALLA.blit(tiempo_texto, (700, ALTURA - 45))

def ranking(volumen=0.2):
    """
    Muestra el top 3 de jugadores con más puntuación.

    Parámetros:
        volumen: el volumen del juego el cual ya viene por defecto inicializado en 0.2 en caso que no se le envie ninguno.
    
    Retorna:
        Nada.
    """
    modo_ranking = True
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)

    while modo_ranking:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_ranking = False
                    seleccion_auto()
        PANTALLA.blit(fondo_ranking, (0, 0))
        ranking = obtener_ranking()
        posiciones = [(350, 250), (350, 300), (350, 350)]

        for i in range(3):
            nombre, puntuacion = ranking[i]
            if i < 3:
                x, y = posiciones[i]
                color_fuente = BLANCO if i == 0 else GRIS
                fuente = pygame.font.SysFont("Arial", 36, bold=True)
                texto_puesto = f"{i+1}. {nombre}"
                text_puesto = fuente.render(texto_puesto, True, color_fuente)
                text_puntuacion = fuente.render(str(puntuacion), True, color_fuente)
                PANTALLA.blit(text_puesto, (x, y))
                PANTALLA.blit(text_puntuacion, (x + 250, y))

        if jugar_boton_centrado_ranking.renderizar(PANTALLA):
            audio_click.play()
            modo_ranking = False
            seleccion_auto(volumen)
        if volver_boton_ranking.renderizar(PANTALLA):
            audio_click.play()
            modo_ranking = False
            iniciar_juego(volumen)
        pygame.display.flip()

def pausa(volume_parametro):
    """
    Muestra el menu de pausa.

    Parámetros:
        volume_parametro: el volumen de la musica.
    
    Retorna:
        retorno: devuelve el volumen y el tiempo transcurrido desde el momento que se inicio el menu de pausa.
    """
    modo_pausa = True
    volumen = volume_parametro
    tiempo_pausa = 0
    tiempo_inicial_pausa = pygame.time.get_ticks()
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)    
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(volumen)
    esta_arrastrando_mouse = False

    while modo_pausa:
        tiempo_pausa = pygame.time.get_ticks()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                modo_pausa = False
                sys.exit()          
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    posicion_mouse = pygame.mouse.get_pos()
                    if posicion_mouse[0] >= 200 and posicion_mouse[0] <= 700 and posicion_mouse[1] >= 300 and posicion_mouse[1] <= 325:
                        esta_arrastrando_mouse = True
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1: 
                    esta_arrastrando_mouse = False
            elif evento.type == pygame.MOUSEMOTION:
                if esta_arrastrando_mouse:
                    posicion_mouse = pygame.mouse.get_pos()
                    volumen = (posicion_mouse[0] - 300) / 400 # Calcula el volumen con la posición del mouse
                    if volumen < 0.0:
                        volumen = 0.0
                    elif volumen > 1.0:
                        volumen = 1.0
                    pygame.mixer.music.set_volume(volumen)
        PANTALLA.blit(fondo_opciones, (0, 0))

        # Renderizar el deslizador
        pygame.draw.rect(PANTALLA, GRIS_2, (300, 300, 400, 30))
        posicion_slider = int(volumen * 400) + 300 
        pygame.draw.circle(PANTALLA, AMARILLO, (posicion_slider, 314), 16) 
        
        if volver_boton_centrado_opciones.renderizar(PANTALLA):
            audio_click.play()
            modo_pausa = False
        if salir_boton_opciones.renderizar(PANTALLA):
            audio_click.play()
            modo_pausa = False
            sys.exit()
        pygame.display.flip()

        tiempo_actual_pausa = pygame.time.get_ticks()
        tiempo_pausa = tiempo_actual_pausa - tiempo_inicial_pausa

    retorno = {
        "volumen": volumen,
        "tiempo_pausa": tiempo_pausa
    }
    return retorno

def chocaste(puntuacion, volumen):
    """
    Muestra el textbox para poder ingresar el nombre y guardar la puntuación.

    Parámetros:
        volumen: el volumen de la musica.
        puntuación: la puntuación conseguida del jugador.
    Retorna:
        Nada.
    """
    modo_chocaste = True
    fuente = pygame.font.SysFont("Arial", 26)
    nombre = ''
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)

    textbox_rect = pygame.Rect(340, 300, 300,32)

    while modo_chocaste:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                modo_chocaste = False
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < MAX_LETRAS:
                        nombre += evento.unicode

        PANTALLA.blit(fondo_perdiste, (0, 0))
        pygame.draw.rect(PANTALLA, BLANCO, textbox_rect, 2)

        texto = fuente.render(nombre, True, BLANCO)
        ingresar_nombre_texto = fuente.render("Ingresar nombre:", True, BLANCO)
        PANTALLA.blit(ingresar_nombre_texto, (textbox_rect.x, textbox_rect.y - 30))
        PANTALLA.blit(texto, (textbox_rect.x +5, textbox_rect.y + 5))

        if guardar_boton_perdiste.renderizar(PANTALLA):
            audio_click.play()
            modo_chocaste = False
            insertar_jugador(nombre, puntuacion)
            ranking(volumen)
        if salir_boton_perdiste.renderizar(PANTALLA):
            audio_click.play()
            modo_chocaste = False
            sys.exit()
        
        pygame.display.flip()

def bucle_de_juego(tipo_auto, volumen_parametro = 0.2):
    """
    Inicia la carrera donde el usuario debe esquivar obstaculos.

    Parámetros:
        volumen: el volumen de la musica la cual ya viene inicializada en 0.2.
        tipo_auto: el tipo de auto seleccionado.
    Retorna:
        Nada.
    """
    # MUSICA
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)
    pygame.mixer.music.play(loops=-1)
    volumen = volumen_parametro
    audio_chocaste = pygame.mixer.Sound(UBICACION_SONIDO_CHOCASTE)
    pygame.mixer.music.set_volume(volumen)
    
    # Texto
    fuente = pygame.font.SysFont("Arial", 100)
    chocaste_texto = fuente.render("CHOCASTE!", 0, ROJO)
    
    # Fondo
    fondo_ancho = fondo_pista.get_width()
    scroll = 0
    velocidad_scroll = 5

    # FPS
    fps = 120
    clock = pygame.time.Clock()
    
    # Jugador
    posicion_y_cambiando = 0
    posicion_x_cambiando = 0
    posicion_default_jugador_x = 0
    posicion_default_jugador_y = 240
    jugador = Vehiculo(posicion_default_jugador_x, posicion_default_jugador_y, tipo_auto)

    # Posicion de los obstaculos
    posiciones_obstaculos = [75, 175, 275, 375]
    posicion_default_obstaculo_x = ANCHO
    num_obstaculos = 1
    obstaculos = []

    # Configuracion de aceite
    posicion_default_aceite_y = random.randrange(100,420)
    posicion_default_aceite_x = ANCHO + 300
    modo_aceite = False
    duracion_aceite = 2000  # 2 segundos
    num_aceites = 1
    aceites = []

    # Sistema de puntuacion
    autos_pasados = 0
    puntuacion = 0
    nivel = 1
    
    juego_corriendo = True
    tiempo = 0

    for i in range(num_obstaculos):
        posicion_y = random.choice(posiciones_obstaculos)
        ocupada = False
        for obstaculo in obstaculos:
            if obstaculo.y == posicion_y:
                ocupada = True
                break
        obstaculo = Obstaculo(posicion_default_obstaculo_x, posicion_y, "imagenes/autos_enemigos/auto{0}.png".format(random.randint(1, 6)))
        obstaculos.append(obstaculo)

    for i in range(num_aceites):
        aceite = Aceite(posicion_default_aceite_x, posicion_default_aceite_y, UBICACION_ACEITE)
        aceites.append(aceite)


    while juego_corriendo:
        milisegundos = clock.tick(fps)
        tiempo += milisegundos

        #Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_corriendo = False
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    volumen = pausa(volumen)
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    if not modo_aceite:
                        posicion_y_cambiando = -3
                    else:
                        posicion_y_cambiando = -0.5
                elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    if not modo_aceite:
                        posicion_x_cambiando = -3
                    else:
                        posicion_x_cambiando = -0.5
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    if not modo_aceite:
                        posicion_x_cambiando = 3
                    else:
                        posicion_x_cambiando = 0.5
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    if not modo_aceite:
                        posicion_y_cambiando = 3
                    else:
                        posicion_y_cambiando = 0.5
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a or evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                    posicion_x_cambiando = 0
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w or evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    posicion_y_cambiando = 0

        jugador.y += posicion_y_cambiando
        jugador.x += posicion_x_cambiando

        # Scroll del fondo
        scroll += velocidad_scroll
        if scroll >= fondo_ancho:
            scroll = 0
        """
        Dibuja el fondo en diferentes posiciones horizontales para lograr el efecto de scroll
        """
        for i in range(-1, int(math.ceil(ANCHO / fondo_ancho)) + 1):
            PANTALLA.blit(fondo_pista, (i * fondo_ancho - scroll, 0))

        # Renderizar jugador
        PANTALLA.blit(jugador.imagen, (jugador.x, jugador.y))
        jugador.actualizar_rectangulo()
        #pygame.draw.rect(PANTALLA, (255, 0, 0), auto.rect, 2) # dibujar rect

        # CREANDO LIMITES DEL AUTO
        if jugador.y > 390:
            jugador.y = 390
        elif jugador.y < 55:
            jugador.y = 55
        if jugador.x > ANCHO - 150:
            jugador.x = ANCHO - 150
        elif jugador.x < 5:
            jugador.x = 5

        # Muestra resultados
        mostrar_resultados(PANTALLA, autos_pasados, puntuacion, nivel, tiempo)

        # Generacion de Aceites
        for aceite in aceites:
            PANTALLA.blit(aceite.imagen, (aceite.x, aceite.y))
            aceite.actualizar_rectangulo()
            #pygame.draw.rect(PANTALLA, (255, 0, 0), aceite.rect, 2)
            aceite.x -= aceite.velocidad
            if aceite.x < -aceite.rect.width:
                aceite.x = ANCHO + 300
                aceite.y = random.randrange(100,420)
            if jugador.rect.colliderect(aceite.rect) and not modo_aceite:
                modo_aceite = True
                tiempo_inicial_aceite = pygame.time.get_ticks()
            if modo_aceite:
                fuente_aceite = pygame.font.SysFont("Arial", 24)
                modo_aceite_texto = fuente_aceite.render("MODO ACEITE", True, ROJO)
                PANTALLA.blit(modo_aceite_texto, (400, ALTURA - 80))
                jugador.x += random.randint(-3, 4)
                jugador.y += random.randint(-3, 4)
                tiempo_actual_aceite = pygame.time.get_ticks()
                if tiempo_actual_aceite - tiempo_inicial_aceite >= duracion_aceite:
                    modo_aceite = False

        # Generacion de obstaculos
        for obstaculo in obstaculos:
            PANTALLA.blit(obstaculo.imagen, (obstaculo.x, obstaculo.y))
            obstaculo.actualizar_rectangulo()
            #pygame.draw.rect(PANTALLA, (255, 0, 0), obstaculo.rect, 2)
            obstaculo.x -= obstaculo.velocidad

            if obstaculo.x < -obstaculo.rect.width:
                posicion_y = random.choice(posiciones_obstaculos)
                while posicion_y in [obst.y for obst in obstaculos]:
                    posicion_y = random.choice(posiciones_obstaculos)
                obstaculo.x = ANCHO
                obstaculo.y = posicion_y
                autos_pasados += 1
                puntuacion += 10
                if autos_pasados % 10 == 0:
                    nivel += 1
                    num_obstaculos += 1
                    if num_obstaculos < 4:
                        posicion_y = random.choice(posiciones_obstaculos)
                        ocupada = False
                        for obstaculo in obstaculos:
                            if obstaculo.y == posicion_y:
                                ocupada = True
                                break
                        while ocupada:
                            posicion_y = random.choice(posiciones_obstaculos)
                            ocupada = False
                            for obstaculo in obstaculos:
                                if obstaculo.y == posicion_y:
                                    ocupada = True
                                    break
                        obstaculo_nuevo = Obstaculo(posicion_default_obstaculo_x, posicion_y, "imagenes/autos_enemigos/auto{0}.png".format(random.randint(1, 6)))
                        obstaculo_nuevo.velocidad = obstaculo.velocidad + 1
                        obstaculo.velocidad += 1
                        obstaculos.append(obstaculo_nuevo)
                    nivel_texto = fuente.render("Nivel: " + str(nivel), True, NEGRO)
                    PANTALLA.blit(nivel_texto, (350, 250))
                    pygame.display.flip()
                    time.sleep(3)
                    tiempo -= 3000
                obstaculo.actualizar_imagen("imagenes/autos_enemigos/auto{0}.png".format(random.randint(1, 6)))

            if jugador.rect.colliderect(obstaculo.rect):
                audio_chocaste.play()
                PANTALLA.blit(chocaste_texto, (235, 250))
                pygame.display.flip()
                time.sleep(3)
                chocaste(puntuacion, volumen)
                juego_corriendo = False

        # Boton de pausa
        if pausar_boton.renderizar(PANTALLA):
            retorno = pausa(volumen)
            volumen = retorno['volumen']
            tiempo -= retorno['tiempo_pausa']
        pygame.display.flip()
