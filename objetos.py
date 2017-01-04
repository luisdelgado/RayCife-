"""
Classe que presenta cada objeto a ser mostrado na cena
"""
from Algebra import Dot, Vector3D, Normal, Normalize, Cross, Parallelogram_Area
from math import sqrt

class Objeto:
    area = 0.0

    def __init__(self, A, B, C, color, ka, kd,ks, kt, n):
        """
        :param vertices - lista de vertices:
        :param faces: lista de Faces
        :param cor: cor do objeto (R,G,B):
        :param ka: coeficiente ambiental
        :param kd: coeficiente difuso
        :param ks: coeficiente especular
        :param kt: coeficiente de transparencia
        :param n: expoente de reflexão especular
        """
        self.A = A # Vertice A
        self.B = B # Vertice B
        self.C = C # Vertice C
        self.normal = Normal(A, B, C)
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kt = kt
        self.n = n

    def intersect(self, ray):

        r = Normalize(ray.d)
        # Checando se o triangulo e o raio são paralelos
        if Dot(r, self.normal) == 0.0:
            # Raio nao intersecta o triangulo
            hit = False
            distance = 0.0
            hit_point = Vector3D(0.0, 0.0, 0.0)

            return (hit, distance, hit_point, self.normal)

        ray_dir = Normalize(ray.d)
        # Calculando o ponto que pode está no plano do triangulo
        t = Dot(self.normal, (self.A - ray.o)) / Dot(ray_dir, self.normal)
        hit_point = ray.get_hitpoint(t)

        if t < 0.0001:
            # Raio nao intersecta o triangulo
            hit = False
            distance = 0.0
            hit_point = Vector3D(0.0, 0.0, 0.0)

            return (hit, distance, hit_point, self.normal)

        # Checando se o Ponto está dentro do triangulo
        # Inside-OutSide Test
        vectorAB = self.B - self.A;
        vectorBC = self.C - self.B;
        vectorCA = self.A - self.C;

        C0 = hit_point - self.A
        C1 = hit_point - self.B
        C2 = hit_point - self.C

        if (Dot(self.normal, Cross(vectorAB, C0)) > 0
                and Dot(self.normal, Cross(vectorBC, C1)) > 0
                and Dot(self.normal, Cross(vectorCA, C2))) > 0:
            #print("Acertou: " + str (vectorAB))
            hit = True
            distance = t
            hit_point = ray.get_hitpoint(t)
            return (hit, distance, hit_point, self.normal)  # tuple

        if (Dot(self.normal, Cross(vectorAB, C0)) < 0
                and Dot(self.normal, Cross(vectorBC, C1)) < 0
                and Dot(self.normal, Cross(vectorCA, C2))) < 0:
            #print("Acertou")
            hit = True
            distance = t
            hit_point = ray.get_hitpoint(t)
            return (hit, distance, hit_point, self.normal)  # tuple

        # Didn't hit the triangule
        hit = False
        distance = 0.0
        hit_point = Vector3D(0.0, 0.0, 0.0)

        return (hit, distance, hit_point, self.normal)


class Light():
    def __init__(self, A, B, C, color, lp):
        self.A = A # Vertice A
        self.B = B # Vertice B
        self.C = C # Vertice C
        self.normal = Normal(A, B, C)
        self.color = color
        self.lp = lp

    def intersect(self, ray):

        r = Normalize(ray.d)
        # Checando se o triangulo e o raio são paralelos
        if Dot(r, self.normal) == 0.0:
            # Raio nao intersecta o triangulo
            hit = False
            distance = 0.0
            hit_point = Vector3D(0.0, 0.0, 0.0)

            return (hit, distance, hit_point, self.normal)

        ray_dir = Normalize(ray.d)
        # Calculando o ponto que pode está no plano do triangulo
        t = Dot(self.normal, (self.A - ray.o)) / Dot(ray_dir, self.normal)
        hit_point = ray.get_hitpoint(t)

        if t < 0.0001:
            # Raio nao intersecta o triangulo
            hit = False
            distance = 0.0
            hit_point = Vector3D(0.0, 0.0, 0.0)

            return (hit, distance, hit_point, self.normal)

        # Checando se o Ponto está dentro do triangulo
        # Inside-OutSide Test
        vectorAB = self.B - self.A;
        vectorBC = self.C - self.B;
        vectorCA = self.A - self.C;

        C0 = hit_point - self.A
        C1 = hit_point - self.B
        C2 = hit_point - self.C

        if (Dot(self.normal, Cross(vectorAB, C0)) > 0
                and Dot(self.normal, Cross(vectorBC, C1)) > 0
                and Dot(self.normal, Cross(vectorCA, C2))) > 0:
            #print("Acertou: " + str (vectorAB))
            hit = True
            distance = t
            hit_point = ray.get_hitpoint(t)
            return (hit, distance, hit_point, self.normal)  # tuple

        if (Dot(self.normal, Cross(vectorAB, C0)) < 0
                and Dot(self.normal, Cross(vectorBC, C1)) < 0
                and Dot(self.normal, Cross(vectorCA, C2))) < 0:
            #print("Acertou")
            hit = True
            distance = t
            hit_point = ray.get_hitpoint(t)
            return (hit, distance, hit_point, self.normal)  # tuple

        # Didn't hit the triangule
        hit = False
        distance = 0.0
        hit_point = Vector3D(0.0, 0.0, 0.0)

        return (hit, distance, hit_point, self.normal)

class ObjectQuadric():
    def __init__(self, a, b, c, d, e, f, g, h, j, k, color, ka,
                 kd, ks, kt, n):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.j = j
        self.k = k
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kt = kt
        self.n = n

    def intersect(self, ray):
        d = ray.d - ray.o

        dx = d[0]
        dy = d[1]
        dz = d[2]

        x0 = ray.o[0]
        y0 = ray.o[1]
        z0 = ray.o[2]

        acoef = 2 * self.f * dx * dz + 2 * self.e * dy * dz + self.c * dz * dz + self.b * dy * dy + self.a * dx * dx + 2 * d * dx * dy

        bcoef = (2 * self.b * y0 * dy + 2 * self.a * x0 * dx + 2 * self.c * z0 * dz) + \
                (2 * self.h * dy + 2 * self.g * dx + 2 * self.j * dz + 2 * d * x0 * dy) + \
                (2 * self.e * y0 * dz + 2 * self.e * z0 * dy + 2 * d * y0 * dx) + \
                (2 * self.f * x0 * dz + 2 * self.f * z0 * dx)

        ccoef = (self.a * x0 * x0 + 2 * self.g * x0 + 2 * self.f * x0 * z0 + self.b * y0 * y0) + \
                (2 * self.e * y0 * z0 + 2 * d * x0 * y0 + self.c * z0 * z0 + 2 * self.h * y0) + \
                (2 * self.j * z0 + self.k)

        ## The following was modified by David J. Brandow to allow for planar

        ## quadrics
        if 1.0 + acoef == 1.0:
            if 1.0 + bcoef == 1.0:
                hit = False
                distance = 0.0
                hit_point = Vector3D(0.0, 0.0, 0.0)

                return (hit, distance, hit_point, self.normal)

            t = (-ccoef) / (bcoef)
        else:
            disc = bcoef * bcoef - 4 * acoef * ccoef

            if 1.0 + disc < 1.0:
                hit = False
                distance = 0.0
                hit_point = Vector3D(0.0, 0.0, 0.0)

                return (hit, distance, hit_point, self.normal)

            root = sqrt(disc)
            t = (-bcoef - root) / (acoef + acoef)

            if t < 0.0:
                t = (-bcoef + root) / (acoef + acoef)

        if (t < 0.001):
            hit = False
            distance = 0.0
            hit_point = Vector3D(0.0, 0.0, 0.0)

            return (hit, distance, hit_point, self.normal)

        hit_point = ray.get_hitpoint(t)
        normal = hit_point - Vector3D(self.a, self.b, self.c)

        return (True, t, hit_point, normal)


        # Didn't hit the Quadradic
        #hit = False
        #distance = 0.0
        #hit_point = Vector3D(0.0, 0.0, 0.0)

        #return (hit, distance, hit_point, self.normal)

