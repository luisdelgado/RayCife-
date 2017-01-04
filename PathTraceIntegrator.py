from Algebra import RGBColour
from Algebra import BLACK, Vector3D, Cross, Normalize, Length, Dot, local_color, Ray, flip_direction, random_direction, WHITE
from objetos import Objeto, Light, ObjectQuadric
import random
from math import sqrt
from math import pow

class PathTraceIntegrator:
    background = BLACK # Cor do Background
    ambient = 0.5

    #Initializer - creates object list
    def __init__(self):
        self.obj_list = []


    #trace light path
    def trace_ray(self, ray, depth, nRefractedInitial):
        difuso = BLACK
        especular = BLACK
        refletido = BLACK
        transmitido = BLACK
        self.nRefractedInitial = nRefractedInitial
        temLuz = 1
        result = BLACK

        # Checando interseções com cada objeto
        dist = 100
        dist2 = 100
        dist3 = 100
        hit = False
        hit2 = False
        hit3 = False
        objeto = 1
        hit_point = Vector3D(0.0, 0.0, 0.0)
        hit_point2 = Vector3D(0.0, 0.0, 0.0)
        hit_point3 = Vector3D(0.0, 0.0, 0.0)
        normal = Vector3D(0.0, 0.0, 0.0)
        normal2 = Vector3D(0.0, 0.0, 0.0)
        normal3 = Vector3D(0.0, 0.0, 0.0)
        objeto2 = 0.0
        objeto3 = 0.0

        for obj in self.obj_list:
            inter = obj.intersect(ray)
            tmp_hit = inter[0]
            distance = inter[1]

            if tmp_hit and distance < dist:
                dist = distance
                objeto = obj
                hit = tmp_hit
                hit_point = inter[2]
                normal = inter[3]

        if hit: ## Se o raio bateu no objeto calculamos a cor do ponto
            if isinstance(objeto, Light):
                return objeto.color
            else:
                if depth == 0 :
                    for l in range (0, 9):
                        lx = random.uniform(-0.9100, 0.9100)
                        lz = random.uniform(-23.3240, -26.4880)
                        shadow_ray2 = Ray(Vector3D(hit_point.x, hit_point.y, hit_point.z), Vector3D(lx, 3.8360, lz))
                        shadow_ray2.d = Vector3D(shadow_ray2.d.x - hit_point.x, shadow_ray2.d.y - hit_point.y,
                                                 shadow_ray2.d.z - hit_point.z)
                        shadow_ray2.d = Normalize(shadow_ray2.d)
                        for obj3 in self.obj_list:
                            inter3 = obj3.intersect(shadow_ray2)
                            tmp_hit3 = inter3[0]
                            distance3 = inter3[1]

                            if tmp_hit3 and distance3 < dist3:
                                dist3 = distance3
                                objeto3 = obj3
                                hit3 = tmp_hit3
                                hit_point3 = inter3[2]
                                normal3 = inter3[3]
                                temLuz = 0
                                if hit3:  ## Se o raio bateu no objeto calculamos a cor do ponto
                                    if isinstance(objeto3, Light):
                                        temLuz = 1

                        if temLuz == 0.0:
                            #if objeto.color == objeto3.color:
                             #   result = local_color(objeto, normal, ray, self.ambient)
                              #  break
                            pass
                        else:
                            result = local_color(objeto, normal, ray, self.ambient)
                            break
                else:
                    result = local_color(objeto, normal, ray, self.ambient)

        else:

            return self.background


        # Calculando os Raios Secúndarios
        ktot = obj.kd + obj.ks + obj.kt
        aleatorio = random.random()*ktot

        if depth > 0:
            if aleatorio < obj.kd:                            ## Raio Difuso
                x = random.random()
                y = random.random()
                dir = random_direction(x, y, normal)
                #dir2 = Normalize(dir)

                # shadow ray
                lx = random.uniform(-0.9100, 0.9100)
                lz = random.uniform(-23.3240, -26.4880)
                shadow_ray = Ray(Vector3D(dir.x, dir.y, dir.z), Vector3D(lx, 3.8360, lz))
                shadow_ray.d = Vector3D(shadow_ray.d.x - dir.x, shadow_ray.d.y - dir.y,
                                         shadow_ray.d.z - dir.z)
                shadow_ray.d = Normalize(shadow_ray.d)
                for obj2 in self.obj_list:
                    inter2 = obj2.intersect(shadow_ray)
                    tmp_hit2 = inter2[0]
                    distance2 = inter2[1]

                    if tmp_hit2 and distance2 < dist2:
                        dist2 = distance2
                        objeto2 = obj2
                        hit2 = tmp_hit2
                        hit_point2 = inter2[2]
                        normal2 = inter2[3]
                        temLuz = 0
                        if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                            if isinstance(objeto2, Light):
                                temLuz = 1

                if temLuz==0:
                    difuso = BLACK
                    #else:
                        #new_ray = Ray(hit_point, Normalize(dir))
                        #difuso = self.trace_ray(new_ray, depth - 1, objeto.kt)
                        #difuso = difuso * objeto2.kt
                else:
                    new_ray = Ray(hit_point, Normalize(dir))
                    difuso = self.trace_ray(new_ray, depth - 1, objeto.kt)
            elif aleatorio < obj.kd + obj.ks:        #         ## Raio especular
                L = Normalize(flip_direction(ray.d))
                N = objeto.normal
                R = (N * (Dot(N, L)) - L) * 2.0
                #R2 = Normalize(R)

                # shadow ray
                lx = random.uniform(-0.9100, 0.9100)
                lz = random.uniform(-23.3240, -26.4880)
                shadow_ray = Ray(Vector3D(R.x, R.y, R.z), Vector3D(lx, 3.8360, lz))
                shadow_ray.d = Vector3D(shadow_ray.d.x - R.x, shadow_ray.d.y - R.y,
                                        shadow_ray.d.z - R.z)
                shadow_ray.d = Normalize(shadow_ray.d)
                for obj2 in self.obj_list:
                    inter2 = obj2.intersect(shadow_ray)
                    tmp_hit2 = inter2[0]
                    distance2 = inter2[1]

                    if tmp_hit2  and distance2 < dist2:
                        dist2 = distance2
                        objeto2 = obj2
                        hit2 = tmp_hit2
                        hit_point2 = inter2[2]
                        normal2 = inter2[3]
                        temLuz = 0
                        if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                            if isinstance(objeto2, Light):
                                temLuz = 1

                if temLuz == 0.0:
                    if objeto2.kt == 0:
                        especular = BLACK
                    else:
                        new_ray = Ray(hit_point, Normalize(R))
                        especular = self.trace_ray(new_ray, depth - 1, objeto.kt)
                        #especular = especular * objeto2.kt
                else:
                    new_ray = Ray(hit_point, Normalize(R))
                    especular = self.trace_ray(new_ray, depth - 1, objeto.kt)
            else:                                               ## Raio Transmitido
                if (objeto.kt > 0):
                    L = Normalize(ray.d)
                    N = objeto.normal
                    if Length(N) != 1:
                        N = Normalize(N)
                    cos1 = Dot(N, flip_direction(L))
                    refletido = L + (N * (2 * cos1))
                    #refletido2 = Normalize(refletido)

                    # shadow ray
                    lx = random.uniform(-0.9100, 0.9100)
                    lz = random.uniform(-23.3240, -26.4880)
                    shadow_ray = Ray(Vector3D(refletido.x, refletido.y, refletido.z), Vector3D(lx, 3.8360, lz))
                    shadow_ray.d = Vector3D(shadow_ray.d.x - refletido.x, shadow_ray.d.y - refletido.y,
                                            shadow_ray.d.z - refletido.z)
                    shadow_ray.d = Normalize(shadow_ray.d)
                    for obj2 in self.obj_list:
                        inter2 = obj2.intersect(shadow_ray)
                        tmp_hit2 = inter2[0]
                        distance2 = inter2[1]

                        if tmp_hit2 and distance2 < dist2:
                            dist2 = distance2
                            objeto2 = obj2
                            hit2 = tmp_hit2
                            hit_point2 = inter2[2]
                            normal2 = inter2[3]
                            temLuz = 0
                            if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                                if isinstance(objeto2, Light):
                                    temLuz = 1

                    if temLuz == 0:
                        if objeto2.kt == 0.0:
                            refletido = BLACK
                        else:
                            new_rayReflected = Ray(hit_point, Normalize(refletido))
                            refletido = self.trace_ray(new_rayReflected, depth - 1, objeto.kt)
                            #refletido = refletido * objeto2.kt
                    else:
                        new_rayReflected = Ray(hit_point, Normalize(refletido))
                        refletido = self.trace_ray(new_rayReflected, depth - 1, objeto.kt)

                    delta = 1-((pow(1.33/objeto.kt,2))*(1-(pow(cos1,2))))
                    if (delta >= 0):
                        cos2 = sqrt(delta)
                        divisao = nRefractedInitial / objeto.kt
                        nRefractedInitial = objeto.kt
                        if (cos1 > 0) :
                            transmitido = (L * divisao) + (N * ((divisao * cos1) - cos2))
                            #transmitido2 = Normalize(transmitido)
                        else:
                            transmitido = (L * divisao) + (N * ((divisao * cos1) + cos2))
                            #transmitido2 = Normalize(transmitido)

                        # shadow ray
                        shadow_ray = Ray(Vector3D(transmitido.x, transmitido.y, transmitido.z), Vector3D(lx, 3.8360, lz))
                        shadow_ray.d = Vector3D(shadow_ray.d.x - transmitido.x, shadow_ray.d.y - transmitido.y,
                                                shadow_ray.d.z - transmitido.z)
                        shadow_ray.d = Normalize(shadow_ray.d)
                        for obj2 in self.obj_list:
                            inter2 = obj2.intersect(shadow_ray)
                            tmp_hit2 = inter2[0]
                            distance2 = inter2[1]

                            if tmp_hit2 and distance2 < dist2:
                                dist2 = distance2
                                objeto2 = obj2
                                hit2 = tmp_hit2
                                hit_point2 = inter2[2]
                                normal2 = inter2[3]
                                temLuz = 0
                                if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                                    if isinstance(objeto2, Light):
                                        temLuz = 1

                        if temLuz == 0:
                            if objeto2.kt == 0.0:
                                transmitido = BLACK
                            else:
                                new_ray = Ray(hit_point, Normalize(transmitido))
                                transmitido = self.trace_ray(new_ray, depth - 1, objeto.kt)
                                #transmitido = transmitido * objeto2.kt
                        else:
                            new_ray = Ray(hit_point, Normalize(transmitido))
                            transmitido = self.trace_ray(new_ray, depth-1, objeto.kt)

        return result + difuso * objeto.kd + especular * objeto.ks + refletido + transmitido * objeto.kt
