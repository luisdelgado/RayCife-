from Algebra import BLACK, Ray, Vector3D, Cross, Normalize, tonemapping
from random import random
import array # para a imagem

class Camera:
    # Initializer
    def __init__(self, eye_point, focal_point, view_distance, up_vector,
                 image_height, image_width, samples_per_pixel):
        self.eye = eye_point
        self.focal = focal_point
        self.view_dist = view_distance
        self.up = up_vector
        self.height = image_height
        self.width = image_width
        self.spp = samples_per_pixel
        # setup orthonormal basis
        #####default values
        self.u = Vector3D(-1.0, 0.0, 0.0)
        self.v = Vector3D(0.0, 1.0, 0.0)
        self.w = Vector3D(0.0, 0.0, -1.0)
        self.compute_uvw()
        # create empty image array
        self.image_array = array.array('B', [0] * (image_width * image_height * 3))

    # Member Functions
    # setup orthonormal basis for camera
    def compute_uvw(self):
        # w
        self.w = self.eye - self.focal
        self.w = Normalize(self.w)
        # u
        self.u = Cross(self.up, self.w)
        self.u = Normalize(self.u)
        # v
        self.v = Cross(self.w, self.u)
        self.v = Normalize(self.v)

        # check for singularity. if conditions met, camera orientations are hardcoded
        # camera looking straight down
        if (self.eye.x == self.focal.x and
                    self.eye.z == self.focal.z and
                    self.focal.y < self.eye.y):
            self.u = Vector3D(0.0, 0.0, 1.0)
            self.v = Vector3D(1.0, 0.0, 0.0)
            self.w = Vector3D(0.0, 1.0, 0.0)

        # camera looking straight up
        if (self.eye.x == self.focal.x and
                    self.eye.z == self.focal.z and
                    self.focal.y > self.eye.y):
            self.u = Vector3D(1.0, 0.0, 0.0)
            self.v = Vector3D(0.0, 0.0, 1.0)
            self.w = Vector3D(0.0, -1.0, 0.0)

    # save pixel to array
    def save_pixel(self, single_pixel, x, y):
        pixel = single_pixel * 255
        pixel.clamp(0.0, 255.0)
        # write to array
        i = ((self.height - y - 1) * self.width + x)
        self.image_array[i * 3 + 0] = int(pixel.r)
        self.image_array[i * 3 + 1] = int(pixel.g)
        self.image_array[i * 3 + 2] = int(pixel.b)

    # save pixel array to file
    def save_image(self, filename):
        # create image file
        image = open(filename, 'wb')
        # write magic number, and filename
        image.write(("P6\n#" + filename).encode())
        # write image width, height and max colour-component value
        image.write(("\n" + str(self.width) + " " + str(self.height) + "\n255\n").encode())
        # write image_array to .ppm file
        image.write(self.image_array.tostring())
        # close .ppm file
        image.close()
        print("Image Saved")

    def get_direction(self, x, y):
        direction = (self.u * x) + (self.v * y) - (self.w * self.view_dist)
        return Normalize(direction)

    # spawns spp number of rays for each pixel
    def render(self, integrator, file_name, depth, tmapping):
        ray = Ray()
        ray.o = self.eye
        pixel = BLACK  # create black pixel
        for x in range(0, self.width):
            for y in range(0, self.height):
                pixel = BLACK  # start at black
                for s in range(0, self.spp):
                    # Obtendo a direção dos raios
                    sp_x = (x + random()) - (self.width / 2.0)
                    sp_y = (y + random()) - (self.height / 2.0)
                    ray.d = self.get_direction(sp_x, sp_y)
                    pixel = pixel + integrator.trace_ray(ray, depth, 1.0)
                pixel = pixel / self.spp
                tonemapping(pixel, tmapping)
                self.save_pixel(pixel, x, y)
            print((x / self.width) * 100, "%")
        # save image to file
        self.save_image(file_name)

