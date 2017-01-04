## leitura dos arquivos
from objetos import Objeto, Light, ObjectQuadric
from Algebra import *

# Cada função trata um tipo diferente do arquivo de configuração
class Read():
    def __init__(self):
        pass

    def eye(self, values):
        return self.__get_float_list(values)

    def size(self, values):
        return  self.__get_float_list(values)

    def ortho(self, values):
        return  self.__get_float_list(values)

    def background(self, values):
        return  self.__get_float_list(values)

    def ambient(self, values):
        return self.__get_float(values)

    def tonemapping(self, values):
        return self.__get_float(values)

    def npaths(self, values):
        return self.__get_float(values)

    def seed(self,  values):
        return self.__get_float(values)

    def deepth(self,  values):
        return self.__get_int(values)

    def object(self, values):
        """
        :param values:
        :return: Lista de objetos de tipo triangulo
        """
        # Obtendo os vertices e faces que se encontram em arquivos separdos
        vertices = self.__get_vertices(values[0])
        faces = self.__get_faces(values[0])

        cor = RGBColour(float(values[1]),
               float(values[2]),
               float(values[3]))

        # Demais propriedades do objeto
        ka = float(values[4])
        kd = float(values[5])
        ks = float(values[6])
        kt = float(values[7])
        n = int(values[8])

        obj_list = []

        for f in faces:
            A = vertices[f[0] - 1]
            B = vertices[f[1] - 1]
            C = vertices[f[2] - 1]

            obj = Objeto(A, B, C, cor, ka, kd, ks, kt, n)
            obj_list.append(obj)

        return obj_list

    def light(self, values):
        # Obtendo os vertices e faces que se encontram em arquivos separdos
        vertices = self.__get_vertices(values[0])
        faces = self.__get_faces(values[0])

        # Cor e intensidade da luz
        color = RGBColour(float(values[1]), float(values[2]), float(values[3]))
        lp = float(values[4])

        light_list = []

        for f in faces:
            A = vertices[f[0] - 1]
            B = vertices[f[1] - 1]
            C = vertices[f[2] - 1]

            li = Light(A,B,C, color, lp)
            light_list.append(li)

        return light_list

    def objectquadric(self, values):
        # Obtendo os vertices e faces que se encontram em arquivos separdos

        a = float(values[0])
        b = float(values[1])
        c = float(values[2])
        d = float(values[3])
        e = float(values[4])
        f = float(values[5])
        g = float(values[6])
        h = float(values[7])
        j = float(values[8])
        k = float(values[9])

        # Lendo Cor
        cor = RGBColour(float(values[10]),
               float(values[11]),
               float(values[12]))

        # Demais propriedades do objeto
        ka = float(values[13])
        kd = float(values[14])
        ks = float(values[15])
        kt = float(values[16])
        n = int(values[17])

        # escrevi só pra não dá erro no arquivo de leitura
        A = Vector3D(d - g, 0.0, 0.0)
        B = Vector3D(0.0, e - h, 0.0)
        C = Vector3D(0.0, 0.0, f - j)
        quad_list = []
        quad = Objeto(A, B, C, cor, ka, kd, ks, kt, n)
        quad_list.append(quad)
        return quad_list

    # Retorna a string contendo o nome do arquivo de saida
    def output(self,values):
        return values[0]

    # retorna uma lista contendo os vertices(Lista de int)
    def __get_faces(self, name):
        faces = []

        f = open ('./src//' + name, 'r')

        for line in f:
            # Pulando linhas em branco
            if len(line) < 2:
                continue

            words = line.split()
            line_type = words[0]  ## Tipo da linha
            values = words[1:]  ## Valores do objeto ou propriedade

            if line_type == 'f':
                vect3 = [int(values[0]),
                         int(values[1]),
                         int(values[2])]

                faces.append(vect3)

        return faces

    # Retorna des vertices(lista de Vector3)
    def __get_vertices(self, name):
        vertices = []
        faces = []

        f = open ('./src//' + name, 'r')

        for line in f:
            # Pulando linhas em branco
            if len(line) < 2:
                continue

            words = line.split()
            line_type = words[0]  ## Tipo da linha
            values = words[1:]  ## Valores do objeto ou propriedade

            if line_type == 'v':
                vect3 = Vector3D(float(values[0]),
                                float(values[1]),
                                float(values[2]))

                vertices.append(vect3)


        return vertices

    # As funções abaixo apenas realizam conversão de tipos em uma lista
    def __get_float_list(self,values):
        return list(map(float, values))

    def __get_float(self, value):
        fst = value[0]

        return float(fst)

    def __get_int(self, value):
        fst = value[0]

        return int(fst)

# Checa o time e designa a função para retornar o valor formatado
def read(t, values):
     read = Read()

    # Chamamos a função com nome read_ + tipo do valor a ser lido(object, light, eye...)
     func = getattr(read, t)
     result = func(values)
     return result
