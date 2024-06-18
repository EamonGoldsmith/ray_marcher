import math

w = 40
h = 20

infinity = 999
infinity_steps = 999

class vec:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def vec_add(a, b):
    return vec(a.x + b.x, a.y + b.y, a.z + b.z)

def vec_coef(a, n):
    return vec(a.x * n, a.y * n, a.z * n)

def vec_mag(v):
    return math.sqrt((v.x ** 2) + (v.y ** 2) + (v.z ** 2))

def normalise(v):
    return vec_coef(v, 1/vec_mag(v))

def draw(buffer):
    for row in buffer:
        tmp = ''
        for pixel in row:
            tmp += pixel
        print(tmp)

def fill_buffer(buffer):
    for y in range(0, h):
        tmp = []
        for x in range(0, w):
            tmp.append('?')
        buffer.append(tmp)

def per_pixel(buffer, shader):
    for y in range(0, h):
        for x in range(0, w):
            buffer[h - y - 1][x] = shader(x, y)

# camera floating above the ground
camera = vec(0, 2, 0)

def dist_est(u):
    # sphere floating above the ground away from the camera
    s = vec(2*math.cos(dt), 2*math.cos(dt), 9 + (3*math.sin(dt)))
    r = 1
    sd = vec_mag(vec_add(u, vec_coef(s, -1))) - r

    # flat infinite plane
    pd = u.y

    return min(sd, pd)

surface_dist = 0.1 
def march_ray(origin, direction, de):
    dist = 0
    for i in range(0, infinity_steps):
        ray = origin
        ray = vec_add(ray, vec_coef(direction, dist))
        est = dist_est(ray)
        dist += est

        if (est < surface_dist):
            return i
        if (dist > infinity):
            break
    # didnt hit anything
    return infinity

def select_char(c):
    if (c > 30):
        return ' '
    elif (c > 15):
        return '.'
    elif (c > 10):
        return '-'
    elif (c > 5):
        return '+'
    elif (c > 3):
        return '='
    else:
        return '#'

def crazy_shader(x, y):
    # rays originate from the camera
    org = camera

    # calculate ray starting direction
    uv_x = (x - (w/2))/w
    uv_y = (y - (h/2))/h
    dr = normalise(vec(uv_x, uv_y, 1))

    dist = march_ray(org, dr, dist_est)

    return select_char(dist)

dt = 0
s = []
fill_buffer(s)

for i in range(0, 100):
    dt += 0.5
    per_pixel(s, crazy_shader)
    draw(s)
