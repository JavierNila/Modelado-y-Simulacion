import random
import pov


# Clase para representar cada celda del ambiente
class Celda:
    def __init__(self):
        self.estado = 3  # Estado inicial (3 = piso)
        self.energia = 0  # Energía de la celda
        self.nido = None  # Nido presente


# Clase para modelar el ambiente
class Patch:
    def __init__(self, ancho, alto):
        self.ancho = ancho  # Ancho de la cuadrícula
        self.alto = alto  # Alto de la cuadrícula
        # Inicializa el ambiente como una matriz de celdas
        self.ambiente = [[Celda() for _ in range(ancho)] for _ in range(alto)]

    def agregar_flores(self, num_flores, energia_flor):
        # ASe agregan flores en las celdas y cada flor tiene una cantidad de energia inicial
        for _ in range(num_flores):
            x, y = random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1)
            celda = self.ambiente[y][x]
            if celda.nido is None:  # Solo agregar flores si no hay un nido
                celda.estado = 0  # Estado 0 = flor (verde)
                celda.energia = energia_flor

    def colocar_nido(self, x, y, colonia):
        celda = self.ambiente[y][x]
        celda.estado = 1 if colonia == 'A' else 2  # Estado 1 = nido A (rojo), 2 = nido B (azul)
        celda.nido = colonia
        celda.energia = 0

# Esta parte la reutilice del codigo de la pandemia
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

                # Cuadrados en lugar de una esferas
                cad += f""" box {{ <{x}, {y}, {z}>, <{x + 1}, {y + 1}, {z + 0.1}> {textura} }} """

        # Guardar el archivo
        with open(archivo, "w") as f:
            f.write(cad)


# Ejecución principal
if __name__ == "__main__":
    ambiente = Patch(50, 50)  # Crear el ambiente con una cuadrícula de 50x50
    ambiente.agregar_flores(50, 50)  # Agregar 50 flores con energía de 50 a celdas aleatorias
    ambiente.colocar_nido(10, 10, 'A')  # Ubicacion del nido A
    ambiente.colocar_nido(40, 40, 'B')  # Ubicacion del nido B
    ambiente.pob2pov()
