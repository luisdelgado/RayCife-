from Algebra import RGBColour
from Algebra import BLACK, Vector3D, Normalize, Length, Dot, local_color, Ray, flip_direction, random_direction
from objetos import Light
import random
from math import sqrt, pow

class PathTraceIntegrator:
    background = BLACK # Cor do Background
    ambient = 0.5

    #Initializer - creates object list
    def __init__(self):
        self.obj_list = []


    #trace light path
    def trace_ray(self, ray, depth, nRefractedInitial, minDepth, eye):
        difuso = BLACK
        especular = BLACK
        transmitido = BLACK
        self.nRefractedInitial = nRefractedInitial
        temLuz = 1
        result = BLACK
        lp = 1.0

        # Checando interseções com cada objeto
        dist = 100
        dist2 = 100
        dist3 = 100
        hit = False
        objeto = 1
        hit_point = Vector3D(0.0, 0.0, 0.0)
        normal = Vector3D(0.0, 0.0, 0.0)

        for obj in self.obj_list:
            inter = obj.intersect(ray)
            tmp_hit = inter[0]
            distance = inter[1]
            if isinstance(objeto, Light):
                lp = objeto.lp

            if tmp_hit and distance < dist:
                dist = distance
                objeto = obj
                hit = tmp_hit
                hit_point = inter[2]
                normal = inter[3]

        if hit: ## Se o raio bateu no objeto calculamos a cor do ponto
            if isinstance(objeto, Light):
                return (objeto.color * objeto.lp, 1)
            else:
                # Só para os primeiros raios
                if depth == minDepth :
                    for l in range (0, 9):
                        lx = random.uniform(-0.9100, 0.9100)
                        lz = random.uniform(-23.3240, -26.4880)
                        luz = Normalize(Vector3D(lx, 3.8360, lz) - hit_point)
                        shadow_ray2 = Ray(Vector3D(hit_point.x, hit_point.y, hit_point.z), luz)
                        for obj3 in self.obj_list:
                            inter3 = obj3.intersect(shadow_ray2)
                            tmp_hit3 = inter3[0]
                            distance3 = inter3[1]

                            if tmp_hit3 and distance3 < dist3:
                                dist3 = distance3
                                objeto3 = obj3
                                hit3 = tmp_hit3
                                temLuz = 0
                                if hit3:  ## Se o raio bateu no objeto calculamos a cor do ponto
                                    if isinstance(objeto3, Light):
                                        temLuz = 1

                        if temLuz == 0.0:
                            pass
                        else:
                            result = local_color(objeto, normal, ray, eye, lp)
                            break
                else:
                    result = local_color(objeto, normal, ray, eye, lp)

        else:

            return (self.background, 0)


        # Calculando os Raios Secúndarios
        ktot = obj.kd + obj.ks + obj.kt
        aleatorio = random.random()*ktot

        if depth > 0:
            if aleatorio < obj.kd:                            ## Raio Difuso
                x = random.random()
                y = random.random()
                dir = random_direction(x, y, normal)

                # shadow ray
                lx = random.uniform(-0.9100, 0.9100)
                lz = random.uniform(-23.3240, -26.4880)
                luz = Normalize(Vector3D(lx, 3.8360, lz) - dir)
                shadow_ray = Ray(Vector3D(dir.x, dir.y, dir.z), luz)
                for obj2 in self.obj_list:
                    inter2 = obj2.intersect(shadow_ray)
                    tmp_hit2 = inter2[0]
                    distance2 = inter2[1]

                    if tmp_hit2 and distance2 < dist2:
                        dist2 = distance2
                        objeto2 = obj2
                        hit2 = tmp_hit2
                        temLuz = 0
                        if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                            if isinstance(objeto2, Light):
                                temLuz = 1

                if temLuz==0:
                    difuso = BLACK
                else:
                    new_ray = Ray(hit_point, Normalize(dir))
                    (difuso, luz) = self.trace_ray(new_ray, depth - 1, objeto.r, minDepth, eye)
            elif aleatorio < obj.kd + obj.ks:        #         ## Raio especular
                L = Normalize(flip_direction(ray.d))
                N = objeto.normal
                R = (N * (Dot(N, L)) - L) * 2.0

                # shadow ray
                lx = random.uniform(-0.9100, 0.9100)
                lz = random.uniform(-23.3240, -26.4880)
                luz = Normalize(Vector3D(lx, 3.8360, lz) - R)
                shadow_ray = Ray(Vector3D(R.x, R.y, R.z), luz)
                for obj2 in self.obj_list:
                    inter2 = obj2.intersect(shadow_ray)
                    tmp_hit2 = inter2[0]
                    distance2 = inter2[1]

                    if tmp_hit2  and distance2 < dist2:
                        dist2 = distance2
                        objeto2 = obj2
                        hit2 = tmp_hit2
                        temLuz = 0
                        if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                            if isinstance(objeto2, Light):
                                temLuz = 1

                if temLuz == 0.0:
                    especular = BLACK
                else:
                    new_ray = Ray(hit_point, Normalize(R))
                    (especular, luz) = self.trace_ray(new_ray, depth - 1, objeto.r, minDepth, eye)
            else:                                               ## Raio Transmitido
                if (objeto.kt > 0):
                    L = Normalize(ray.d)
                    N = objeto.normal
                    if Length(N) != 1:
                        N = Normalize(N)
                    cos1 = Dot(N, flip_direction(L))
                    divisao = nRefractedInitial / objeto.r
                    delta = 1-((pow(divisao,2))*(1-(pow(cos1,2))))
                    if (delta >= 0):
                        cos2 = sqrt(delta)
                        if ( nRefractedInitial != objeto.r):
                            nRefractedInitial = objeto.r
                        else:
                            nRefractedInitial = 1.0
                        if (cos1 > 0) :
                            transmitido = (L * divisao) + (N * ((divisao * cos1) - cos2))
                        else:
                            transmitido = (L * divisao) + (N * ((divisao * cos1) + cos2))

                        # shadow ray
                        lx = random.uniform(-0.9100, 0.9100)
                        lz = random.uniform(-23.3240, -26.4880)
                        luz = Normalize(Vector3D(lx, 3.8360, lz) - transmitido)
                        shadow_ray = Ray(Vector3D(transmitido.x, transmitido.y, transmitido.z), luz)
                        for obj2 in self.obj_list:
                            inter2 = obj2.intersect(shadow_ray)
                            tmp_hit2 = inter2[0]
                            distance2 = inter2[1]

                            if tmp_hit2 and distance2 < dist2:
                                dist2 = distance2
                                objeto2 = obj2
                                hit2 = tmp_hit2
                                temLuz = 0
                                if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                                    if isinstance(objeto2, Light):
                                        temLuz = 1

                        if temLuz == 0:
                            transmitido = BLACK
                        else:
                            new_ray = Ray(hit_point, Normalize(transmitido))
                            (transmitido, luz) = self.trace_ray(new_ray, depth-1,  nRefractedInitial, minDepth, eye)

        return result + difuso * objeto.kd + especular * objeto.ks + transmitido * objeto.kt , 0
