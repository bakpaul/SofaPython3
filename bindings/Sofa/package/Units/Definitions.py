from .Core import *


### Primary units
DimensionLess = NeutralUnit()
s = PrimaryUnit("s")        # time
m = PrimaryUnit("m")        # length
kg = PrimaryUnit("kg")      # mass
A = PrimaryUnit("A")        # electric current
K = PrimaryUnit("K")        # temperature
mol = PrimaryUnit("mol")    # amount of substance
cd = PrimaryUnit("cd")      # luminous intensity


### (some) Derived units
v = m/s                     # velocity
a = v/s                     # acceleration
N = kg*a                    # force (Newton)
Pa = N/(m**2)               # pressure (Pascal)
tho = m*N                   # torque 
J = kg*m**2/s**2            # energy (Joule)
W = J/s                     # power (Watt)


## Scaled primary units
nm = ScaledUnit(m, 1e-9)
µm = ScaledUnit(m, 1e-6)
mm = ScaledUnit(m, 1e-3)
cm = ScaledUnit(m, 1e-2)
dm = ScaledUnit(m, 1e-1)
km = ScaledUnit(m, 1e3)

ns = ScaledUnit(s, 1e-9)
µs = ScaledUnit(s, 1e-6)
ms = ScaledUnit(s, 1e-3)

µg = ScaledUnit(kg, 1e-9)
mg = ScaledUnit(kg, 1e-6)
g = ScaledUnit(kg, 1e-3)
t = ScaledUnit(kg, 1e3)

## Scaled derived units
nN = ScaledUnit(N, 1e-9)
µN = ScaledUnit(N, 1e-6)
mN = ScaledUnit(N, 1e-3)
cN = ScaledUnit(N, 1e-2)
dN = ScaledUnit(N, 1e-1)
kN = ScaledUnit(N, 1e3)
MN = ScaledUnit(N, 1e6)
GN = ScaledUnit(N, 1e9)


nPa = ScaledUnit(Pa, 1e-9)
µPa = ScaledUnit(Pa, 1e-6)
mPa = ScaledUnit(Pa, 1e-3)
cPa = ScaledUnit(Pa, 1e-2)
dPa = ScaledUnit(Pa, 1e-1)
kPa = ScaledUnit(Pa, 1e3)
MPa = ScaledUnit(Pa, 1e6)
GPa = ScaledUnit(Pa, 1e9)

mJ = ScaledUnit(J, 1e-3)
cJ = ScaledUnit(J, 1e-2)
dJ = ScaledUnit(J, 1e-1)
kJ = ScaledUnit(J, 1e3)
MJ = ScaledUnit(J, 1e6)
GJ = ScaledUnit(J, 1e9)

mW = ScaledUnit(W, 1e-3)
cW = ScaledUnit(W, 1e-2)
dW = ScaledUnit(W, 1e-1)
kW = ScaledUnit(W, 1e3)
MW = ScaledUnit(W, 1e6)
GW = ScaledUnit(W, 1e9)





