import math
import random

def v(*args, **kwargs):
    return Vector(*args, **kwargs)

def v_zero():
    return Vector(0, 0, 0)

def v_rand():
    return Vector(random.random(), random.random(), random.random()) - v(0.5, 0.5, 0.5)

# TODO use numpy or sth
class Vector:
    def __init__(self, x, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


    def __abs__(self):
        return self.mag()

    def mag(self):
        return math.sqrt(self.mag_sq())

    def mag_sq(self):
        return self.x**2 + self.y**2 + self.z**2


    def __add__(self, other):
        return Vector(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z)

    def __mul__(self, factor):
        return Vector(
                factor*self.x,
                factor*self.y,
                factor*self.z)

    def __sub__(self, other):
        return other*(-1)+self


    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def is_colinear(self, other):
        return abs(Vector.dot(self, other)) == (abs(self)*abs(other))

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Particle:
    def __init__(self, mass, pos = v_zero(), velocity = v_zero()):
        self.mass = mass
        self.position = pos
        self.velocity = velocity

    def move(self, dt):
        self.position += self.velocity*dt

    @property
    def momentum(self):
        return self.velocity * self.mass

    @property
    def kinetic_energy(self):
        return 1/2 * self.mass * self.velocity.mag_sq()

    def __str__(self):
        return f"Particle m={self.mass} @{self.position} v={self.velocity}"

def rebase(pos, vel, p):
    return Particle(
            mass = p.mass,
            pos = p.position - pos,
            velocity = p.velocity - vel,
            )

class System:
    def __init__(self, ps):
        self._particles = ps


    def kinetic_energy(self):
        return sum(p.kinetic_energy for p in self._particles)

    def momentum(self):
        return sum((p.momentum for p in self._particles), v_zero())

    def com(self):
        return sum((p.position*p.mass for p in self._particles), v_zero())

    def move(self, dt):
        return [p.move(dt) for p in self._particles]

    def sim_for(self, end_t):
        t = 0
        dt = self.next_collision_dt()
        init_p = self.momentum()
        init_k = self.kinetic_energy()
        print(dt)
        while t + dt < end_t:
            self.move(dt)
            t += dt

            for p, q in self.pairs:
                if abs(p.position-q.position) < 1:
                    collide(p, q)
                    if False:
                        print(f'\nbump\n\t{p}\n\t{q}')
                        print(f"\tt={t}")
                        print(self.momentum())
                        print(self.kinetic_energy())

            dt = self.next_collision_dt()

        print()
        print("init")
        print(init_p, init_k)
        print(self.momentum(), self.kinetic_energy())
        print(t)


    @property
    def pairs(self):
        for i, p in enumerate(self._particles):
            for j, q in enumerate(self._particles):
                if i >= j:
                    continue

                yield (p, q)


    def next_collision_dt(self):
        t = float("Inf")

        return min(future_collision_time(p, q) for p, q in self.pairs)

        return t


def collide(p1, p2, dt = 0):
    if dt != 0:
        return collide(p1.move(dt), p2.move(dt))

    assert abs(p1.position - p2.position) < 1, "Particles aren't colliding..."

    ps = System([p1, p2])
    momentum = ps.momentum()
    com_vel = momentum*(1/(p1.mass+p2.mass))

    p1.velocity = ((com_vel - p1.velocity) + com_vel)
    p2.velocity = ((com_vel - p2.velocity) + com_vel)

def collision_time(p1, p2):
    ps = System([p1, p2])
    momentum = ps.momentum()
    com = ps.com()

    p1_adj = rebase(com, momentum, p1)
    p2_adj = rebase(com, momentum, p2)

    t_from_com = abs(p1.position)/abs(p1.velocity)
    p1_adj.move(t_from_com)
    p2_adj.move(t_from_com)

    if abs(p1_adj.position-p2_adj.position) < 1:
        return t_from_com

    return float("Inf")

def future_collision_time(p1, p2):
    t = collision_time(p1, p2)
    if t <= 0:
        return float("Inf")
    return t



def p_in_box(n = 10):
    return System(
            [
                Particle(
                    mass = 1.0,
                    pos = v_rand()*2,
                    velocity = v_rand()
                    )
                for i in range(n)]
            )


if __name__ == "__main__":
    ps = p_in_box(250)
    t = 0
    dt = 1
    #print([str(p.position) for p in ps._particles])
    #print([str(p.velocity) for p in ps._particles])
    print(ps.kinetic_energy())
    print(ps.momentum())
    print(ps.com())

    ps.sim_for(1000)
    print()

    #print([str(p.position) for p in ps._particles])
    #print([str(p.velocity) for p in ps._particles])
    print(ps.kinetic_energy())
    print(ps.momentum())
    print(ps.com())



    print("done")
