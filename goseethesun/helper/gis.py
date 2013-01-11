__author__ = 'tmaul'

#    from http://code.google.com/p/pysatel/source/browse/trunk/coord.py?r=22

from math import pow, degrees, sqrt, atan, atan2, cos, sin, radians

a = 6378.137
b = 6356.7523142
esq = 6.69437999014 * 0.001
e1sq = 6.73949674228 * 0.001
f = 1 / 298.257223563

def cbrt(x):
    if x >= 0:
        return pow(x, 1.0/3.0)
    else:
        return -pow(abs(x), 1.0/3.0)

def ecef2geodetic(x, y, z):
    """Convert ECEF coordinates to geodetic.
    J. Zhu, "Conversion of Earth-centered Earth-fixed coordinates \
    to geodetic coordinates," IEEE Transactions on Aerospace and \
    Electronic Systems, vol. 30, pp. 957-961, 1994."""
    r = sqrt(x * x + y * y)
    Esq = a * a - b * b
    F = 54 * b * b * z * z
    G = r * r + (1 - esq) * z * z - esq * Esq
    C = (esq * esq * F * r * r) / (pow(G, 3))
    S = cbrt(1 + C + sqrt(C * C + 2 * C))
    P = F / (3 * pow((S + 1 / S + 1), 2) * G * G)
    Q = sqrt(1 + 2 * esq * esq * P)
    r_0 =  -(P * esq * r) / (1 + Q) + sqrt(0.5 * a * a*(1 + 1.0 / Q) -\
                                           P * (1 - esq) * z * z / (Q * (1 + Q)) - 0.5 * P * r * r)
    U = sqrt(pow((r - esq * r_0), 2) + z * z)
    V = sqrt(pow((r - esq * r_0), 2) + (1 - esq) * z * z)
    Z_0 = b * b * z / (a * V)
    h = U * (1 - b * b / (a * V))
    lat = atan((z + e1sq * Z_0) / r)
    lon = atan2(y, x)
    return degrees(lat), degrees(lon)

def geodetic2ecef(lat, lon, alt):
    """Convert geodetic coordinates to ECEF."""
    lat, lon = radians(lat), radians(lon)
    xi = sqrt(1 - esq * sin(lat))
    x = (a / xi + alt) * cos(lat) * cos(lon)
    y = (a / xi + alt) * cos(lat) * sin(lon)
    z = (a / xi * (1 - esq) + alt) * sin(lat)
    return Vector(x, y, z)


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x;
        self.y = y;
        self.z = z;

    def dot(self, v):
        return pow(self.x + v.x, 2) + pow(self.y + v.y, 2) + pow(self.z + v.z, 2)

    def length(self):
        return sqrt( self.dot(self));

    def unit(self):
        l = sqrt( self / self.length() )

    def __div__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return str((self.x, self.y, self.z))

    def __repr__(self):
        return self.__str__()