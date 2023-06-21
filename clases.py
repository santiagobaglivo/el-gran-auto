import pygame

class ObjetoJuego:
	"""
	Clase padre que representa un objeto del juego.
	"""
	def __init__(self, x, y, imagen):
		"""
		Constructor de la clase ObjetoJuego

		x: coordenada x del objeto.
		y: coordenada y del objeto.
		imagen: ruta de la imagen del objeto.
		"""	
		pygame.sprite.Sprite.__init__(self)
		self.imagen = pygame.image.load(imagen).convert_alpha()
		self.imagen = pygame.transform.smoothscale(self.imagen, (150, 150))
		self.x = x
		self.y = y
		self.width = 150
	def actualizar_rectangulo(self):
		"""
		Actualiza el rectangulo del objeto segun su  posicion y dimensiones.
		"""
		self.rect = self.imagen.get_rect()
		ancho_rectangulo = self.rect.width
		altura_rectangulo = self.rect.height
		self.rect.topleft = (self.x, self.y)
		self.rect.width = ancho_rectangulo - 20  
		self.rect.height = 60
		self.rect.center = (self.x + ancho_rectangulo // 2, self.y + altura_rectangulo // 2)  # Centrar el rectángulo

class Vehiculo(ObjetoJuego):
	"""
	Clase que representa el vehiculo del jugador. Hereda la clase ObjetoJuego
	"""
	def __init__(self, x, y, tipo_auto):
		"""
		Constructor de la clase Vehiculo.
		
		x: coordenada x del objeto.
		y: coordenada y del objeto.
		tipo_auto: el tipo de auto seleccionado.
		"""	
		super().__init__(x, y, tipo_auto)

class Aceite(ObjetoJuego):
	"""
	Clase que representa la aceite del juego. Hereda la clase ObjetoJuego
	"""
	def __init__(self, x, y, imagen):
		"""
		Constructor de la clase Aceite.

		x: coordenada x del objeto.
		y: coordenada y del objeto.
		imagen: ruta de la imagen del objeto.
		"""    
		super().__init__(x, y, imagen)
		self.imagen = pygame.transform.smoothscale(self.imagen, (75,75))
		self.velocidad = 6

class Obstaculo(ObjetoJuego):
	"""
	Clase que representa los obstaculos del juego. Hereda la clase ObjetoJuego
	"""	
	def __init__(self, x, y, tipo_obstaculo):
		"""
		Constructor de la clase Obstaculo.
		
		x: coordenada x del objeto.
		y: coordenada y del objeto.
		tipo_obstaculo: el tipo de auto seleccionado.
		"""
		super().__init__(x, y, tipo_obstaculo)
		self.tipo_obstaculo = tipo_obstaculo
		self.velocidad = 6
	def actualizar_imagen(self, imagen):
		"""
		Actualiza y reescala la imagen.
		"""
		self.imagen = pygame.image.load(imagen).convert_alpha()
		self.imagen = pygame.transform.smoothscale(self.imagen, (150, 150))

class Boton():
	"""
    Clase que representa un botón interactivo en el juego.
    """
	def __init__(self, imagen, escala, x, y):
		"""
        Constructor de la clase Boton.

        imagen: Imagen del botón.
        escala: Escala de la imagen del botón.
        x: Coordenada x de la posición del botón.
        y: Coordenada y de la posición del botón.
        """
		super(Boton, self).__init__()
		self.escala = escala
		self.imagen = pygame.transform.smoothscale(imagen, self.escala)
		self.rect = self.imagen.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clickeado = False

	def actualizar_imagen(self, imagen):
		"""
        Actualiza la imagen del botón.

        imagen: Nueva imagen del botón.
        """
		self.imagen = pygame.transform.smoothscale(imagen, self.escala)

	def renderizar(self, pantalla):
		"""
        Renderiza el botón en la pantalla y chequea si se clickea.

        pantalla: Superficie de la pantalla donde se renderiza el botón.
        
		Retorna: 
		
		accionar: Un valor booleano que indica si se ha realizado una acción al hacer clic en el botón.
        """
		accionar = False
		posicion = pygame.mouse.get_pos()
		if self.rect.collidepoint(posicion):
			if pygame.mouse.get_pressed()[0] and not self.clickeado:
				accionar = True
				self.clickeado = True

			if not pygame.mouse.get_pressed()[0]:
				self.clickeado = False

		pantalla.blit(self.imagen, self.rect)
		return accionar 

