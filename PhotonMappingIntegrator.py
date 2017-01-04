from Algebra import Vector3D
from math import sqrt, cos, pi
from random import uniform
import Photon

class PhotonMappingIntegrator:
    numeroPhotons = 2.0
    contador = 0
    depthOriginal = 4

    # Initializer - creates object list
    def __init__(self):
        self.obj_list = []
        self.photons_list = []

    #photon path
    def photon_ray(self, ray, depth):

        # Checando interseções com cada objeto
        dist = 100
        hit = False
        objeto = 1
        hit_point = Vector3D(0.0, 0.0, 0.0)
        normal = Vector3D(0.0, 0.0, 0.0)

        for n in self.numeroPhotons :

            for obj in self.obj_list:

                # setado com os valores da fonte de luz para o primeiro caso
                if self.depth == 4 :
                    inter = obj.intersect(-0.9100, 3.8360 -23.3240), (0.0, -1.0, 0.0)
                else:
                    inter = obj.intersect(ray)

                tmp_hit = inter[0]
                distance = inter[1]

                if tmp_hit and distance < dist:
                    dist = distance
                    objeto = obj
                    hit = tmp_hit
                    hit_point = inter[2]
                    normal = inter[3]

            if hit: ## Se o raio bateu no objeto adicionamos o photon a estrutura de dados
                R1 = uniform(0.0, 1.0)
                R2 = uniform(0.0, 1.0)
                direcaoPhi = 1/cos(sqrt(R1))
                direcaoTheta = 2*pi*R2
                R = 1.0
                T = 1.0
                self.photons_list[self.contador] = Photon(hit_point, R*1.0/self.numeroPhotons, T*1.0/self.numeroPhotons, direcaoPhi, direcaoTheta)
                self.contador = self.contador +1

                # chamar raio secundário
                # http://www.cs.cmu.edu/afs/cs/academic/class/15462-s12/www/lec_slides/lec18.pdf