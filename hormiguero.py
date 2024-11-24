import random
import pov

# Clase para representar cada celda del ambiente
class Celda:
    def __init__(self):
        self.estado = 3  # Estado inicial (3 = piso vacío)
        self.energia = 0  # Energía asociada a la celda
        self.nido = None  # Identificador del nido presente en la celda

# Clase para modelar el ambiente
class Patch:
    
    def pob2pov(self, archivo="hormiguero.pov"):
        cad = pov.povBasico()
        cad += pov.povLuz(1000, 1000, 1000, 1, 1, 1)
        cad += pov.povCamara(self.ancho // 2, self.alto // 2, self.alto * 1.2, self.ancho // 2, self.alto // 2, 0)

        for y in range(self.alto):
            for x in range(self.ancho):
                celda = self.ambiente[y][x]
                z = 0  # Altura fija para todas las celdas

                if celda.estado == 0:  # Flor
                    textura = "texture{pigment{color rgb <0,1,0>}}"
                elif celda.estado == 1:  # Nido A
                    textura = "texture{pigment{color rgb <1,0,0>}}"
                elif celda.estado == 2:  # Nido B
                    textura = "texture{pigment{color rgb <0,0,1>}}"
                elif celda.estado == 3:  # Piso blanco
                    textura = "texture{pigment{color rgb <1,1,1>}}"
                elif celda.estado == 4:
                    textura = "texture{pigment{color rgb <0.722, 0.443, 0.271>}}"
                elif celda.estado == 5:
                    textura = "texture{pigment{color rgb <0.431, 0.302, 0.788>}}"

                # Cuadrados en lugar de una esferas
                cad += f""" box {{ <{x}, {y}, {z}>, <{x + 1}, {y + 1}, {z + 0.1}> {textura} }} """
        return cad
    
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ambiente = [[Celda() for _ in range(ancho)] for _ in range(alto)]
        self.nidos = {}

    def agregar_flores(self, num_flores, energia_flor):
        for _ in range(num_flores):
            x, y = random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1)
            celda = self.ambiente[y][x]
            if celda.nido is None and celda.estado == 3:
                celda.estado = 0  # Estado 0 = flor
                celda.energia = energia_flor

    def colocar_nido(self, x, y, colonia):
        celda = self.ambiente[y][x]
        celda.estado = 1 if colonia == 'A' else 2  # Estado 1 = nido A, 2 = nido B
        celda.nido = colonia
        self.nidos[colonia] = Nido(colonia, (x, y))

    def obtener_nido(self, colonia):
        return self.nidos.get(colonia)

    def obtener_posicion_nido(self, colonia):
        if colonia in self.nidos:
            return self.nidos[colonia].posicion
        return None

    def mostrar_estado(self):
        print("\nEstado del ambiente:")
        for fila in self.ambiente:
            print(" ".join(str(celda.estado) for celda in fila))

class Nido:
    def __init__(self, colonia, posicion):
        self.colonia = colonia
        self.posicion = posicion
        self.comidaAlmacenada = 0

    def almacenarComida(self, cantidad):
        self.comidaAlmacenada += cantidad

class Hormiga:
    def __init__(self, colonia, energia, patch):
        self.colonia = colonia
        self.energia = energia
        self.tieneComida = False
        self.viva = True
        self.posicion = patch.obtener_posicion_nido(colonia)
        self.patch = patch

    def buscarComida(self):
        if not self.viva:
            return

        # Movimiento aleatorio
        x, y = self.posicion
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        nueva_x, nueva_y = x + dx, y + dy

        # Validar límites del ambiente
        if 0 <= nueva_x < self.patch.ancho and 0 <= nueva_y < self.patch.alto:
            celda_actual = self.patch.ambiente[y][x]
            nueva_celda = self.patch.ambiente[nueva_y][nueva_x]

            # Si la nueva celda tiene una flor
            if nueva_celda.estado == 0:
                nueva_celda.estado = 3  # Cambiar flor a piso vacío
                nueva_celda.energia = 0  # La flor ha sido recolectada
                self.tieneComida = True
                self.energia += 20  # Ganar energía por recolectar comida
                print(f"Hormiga de colonia {self.colonia} recolectó comida en ({nueva_x}, {nueva_y}).")

            # Evitar sobrescribir el estado del nido
            if celda_actual.estado not in (1, 2):
                celda_actual.estado = 3  # Celda anterior se convierte en piso vacío
            if nueva_celda.estado not in (1, 2):
                nueva_celda.estado = 4 if self.colonia == 'A' else 5  # Nueva celda toma el estado de la hormiga
            self.posicion = (nueva_x, nueva_y)  # Actualizar posición

        # Reducir energía por movimiento
        self.energia -= 1
        if self.energia <= 0:
            self.viva = False
            print(f"Hormiga de colonia {self.colonia} ha muerto.")

    def regresarAlNido(self):
        if not self.viva or not self.tieneComida:
            return

        x, y = self.posicion
        nido_x, nido_y = self.patch.obtener_posicion_nido(self.colonia)

        # Movimiento hacia el nido
        if x < nido_x:
            x += 1
        elif x > nido_x:
            x -= 1

        if y < nido_y:
            y += 1
        elif y > nido_y:
            y -= 1

        self.posicion = (x, y)

        # Si llegó al nido, deposita la comida
        if (x, y) == (nido_x, nido_y):
            nido = self.patch.obtener_nido(self.colonia)
            nido.almacenarComida(1)
            self.tieneComida = False
            print(f"Hormiga de colonia {self.colonia} depositó comida en el nido.")


"""
# Ejecución principal
if __name__ == "__main__":
    ambiente = Patch(50, 50)  # Crear el ambiente con una cuadrícula de 50x50
    ambiente.agregar_flores(50, 50)  # Agregar 50 flores con energía de 50 a celdas aleatorias
    ambiente.colocar_nido(10, 10, 'A')  # Ubicacion del nido A
    ambiente.colocar_nido(40, 40, 'B')  # Ubicacion del nido B
    ambiente.pob2pov()

Esta ejecución ya no funciona por las modificaciones que hice de las clases, la ejecución principal será distinta
"""

