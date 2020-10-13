from lib import *
from sphere import *
from math import pi, tan
import random

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
BG = color(107,156,245)


class Raytracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.background_color = BLACK
    self.scene = []
    self.clear()
    self.light = None

  def clear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)


  def point(self, x, y, c = None):
    try:
      self.pixels[y][x] = c or self.current_color
    except:
      pass

  def cast_ray(self, orig, direction):
    material, intersect = self.scene_intersect(orig, direction)

    if material is None:
      return self.background_color
    
    light_dir = norm(sub(self.light.position, intersect.point))
    light_distance = length(sub(self.light.position, intersect.point))

    offset_normal = mul(intersect.normal, 1.1)  # avoids intercept with itself
    shadow_orig = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
    shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
    shadow_intensity = 0

    if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
      shadow_intensity = 0.9

    intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

    reflection = reflect(light_dir, intersect.normal)
    specular_intensity = self.light.intensity * (
      max(0, -dot(reflection, direction))**material.spec
    )

    diffuse = material.diffuse * intensity * material.albedo[0]
    specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
    return diffuse + specular

  def scene_intersect(self, orig, direction):
      zbuffer = float('inf')

      material = None
      intersect = None

      for obj in self.scene:
        hit = obj.ray_intersect(orig, direction)
        if hit is not None:
          if hit.distance < zbuffer:
            zbuffer = hit.distance
            material = obj.material
            intersect = hit

      return material, intersect

  def render(self, stereogram=False):
    fov = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * self.width/self.height
        j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
        direction = norm(V3(i, j, -1))
        
        if(stereogram):
          eye1 = self.cast_ray(V3(0.4,0,0), direction)
          eye2 = self.cast_ray(V3(-0.4,0,0), direction)
          if not eye1.equals(self.background_color):
            eye1 = eye1*0.57 + color(100,0,0)                                    
          if not eye2.equals(self.background_color):
            eye2 = eye2*0.57 + color(0,0,100)                                            
          eye_sum = eye1 + eye2
          self.pixels[y][x] = eye_sum
        else:
          self.pixels[y][x] = self.cast_ray(V3(1,0,0), direction) 
  


#global
eye = Material(diffuse = BLACK, albedo = (0.6,  0.3), spec = 35)

#left bear
body1 = Material(diffuse = color(255,255,255), albedo = (1, 1, 1), spec = 30)


#right bear
body2 = Material(diffuse = color(240, 175, 137), albedo = (1, 1, 1), spec = 30)
body2a = Material(diffuse = color(201, 64, 26), albedo = (1, 1, 1), spec = 30) 
body2b = Material(diffuse = color(175, 85, 45), albedo = (1, 1, 1), spec = 15)



#init
r = Raytracer(1000, 1000)

#light
r.light = Light(
  position=V3(0,0,20),
  intensity=1
)


r.scene = [
    
    #ears
    Sphere(V3(3.4, 2.9, -9), 0.4, body2b),
    Sphere(V3(-3.4, 2.9, -9), 0.4, body1),

    Sphere(V3(1.4, 2.9, -9), 0.4, body2b),
    Sphere(V3(-1.4, 2.9, -9), 0.4, body1),
    
    #faces
    Sphere(V3(2.5, 2, -10), 1.5, body2),
    Sphere(V3(-2.5, 2, -10), 1.5, body1),
    #eyes
    Sphere(V3(-2.4, 2.1, -8), 0.1, eye),
    Sphere(V3(2.4, 2.1, -8), 0.1, eye),

    Sphere(V3(-1.7, 2.1, -8), 0.1, eye),
    Sphere(V3(1.7, 2.1, -8), 0.1, eye),
    #noses
    Sphere(V3(2.4, 1.5, -9), 0.65, body2b),
    Sphere(V3(-2.4, 1.5, -9), 0.65, body1),
    #tip of nose
    Sphere(V3(-2.1, 1.7, -8), 0.1, eye),
    Sphere(V3(2.1, 1.7, -8), 0.1, eye),

    #belly
    Sphere(V3(2.5, -1, -10), 1.75, body2a),
    Sphere(V3(-2.5, -1, -10), 1.75, body1),

    #limbs
      #arms

    Sphere(V3(4, 0, -9), 0.6, body2),
    Sphere(V3(-4, 0, -9), 0.6, body1),

    Sphere(V3(1, 0, -9), 0.6, body2),
    Sphere(V3(-1, 0, -9), 0.6, body1),

      #legs

    Sphere(V3(4, -2.5, -9), 0.70, body2),
    Sphere(V3(-4, -2.5, -9), 0.70, body1),

    Sphere(V3(1, -2.5, -9), 0.70, body2),
    Sphere(V3(-1, -2.5, -9), 0.70, body1),    
]
r.render(stereogram=True)
r.write('out.bmp') 