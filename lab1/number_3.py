import math
import matplotlib.pyplot as pl

# === Несколько общих формул cntrC со второго номера === #
# ===          Горнер, границы, интервалы            === #

def horner(coeffs, x):
  n = len(coeffs)
  b = [0.0] * n
  b[0] = coeffs[0]
  for i in range(1,n):
    b[i] = b[i-1] * x + coeffs[i]
  return b

def upper_bnd(coeffs):
  c = coeffs.copy()
  if c[0] < 0:
    c = [-i for i in c] 
  L = 1
  while L <= 500:
    vals = horner(c, L)
    if all(v >= 0 for v in vals):
        return L
    L += 1
  return None

def lower_bnd(coeffs):
  c_neg = [coeffs[i] *((-1) ** (len(coeffs) - 1 - i)) for i in range(len(coeffs))]
  L = upper_bnd(c_neg)
  if L is not None:
    return -L
  return None

def find_intervals(f, a, b, h=0.1):
  x = a
  intervals = []
  while x < b:
    if f(x) * f(x + h) <=0:
      intervals.append((x,x+h))
    x += h
  return intervals

# === Новые общие функции === #

# --- а) Метод Хорд --- #

def chord_method(f, a, b, eps=0.001):
  iters = 0
  while True:
    x = b - f(b) * (b - a) / (f(b) - f(a))
    iters+=1
    if abs(x_next - x_curr) < eps:
      return x_next, iters
    a = x


# === Сам третий номер === #

# --- Уравнение а) 2x-lg(x)-7=0 --- #
print("a) 2x - lg(x) - 7 = 0")
f_a = lambda x: 2 * x - math.log(x) - 7
# ОО x > 0 -> от 0.1 до 10
intervals_a = find_intervals(f_a, 0.1, 10, 0.1)
print(f"Bounds with roots: {intervals_a}")
a_a, b_a = 4.2, 4.3
root_chord, iters_chord = chord_method(f_a, a_a, b_a)
print(f"Root (chord method): {root_chord}. \nIterations count: {iters_chord}")

# --- Уравнение б) x^3-3x^2+6x-5=0 --- #
print("\nb) x^3 - 3x^2 + 6x - 5 = 0")
coeffs_b = [1.0, -3.0, 6.0, -5.0]
up_b = upper_bnd(coeffs_b)
dwn_b = lower_bnd(coeffs_b)
print(f"Bounds from Horner: [{dwn_b} : {up_b}]")
f_b = lambda x: x**3 - 3 * x**2 + 6 * x - 5
intervals_b = find_intervals(f_b, dwn_b, up_b, 0.1)
print(f"Bounds with roots: {intervals_b}")

# --- Уравнение в) 2x^3+9x^2-6=0 --- #
print("\nc) 2x^3 + 9x^2 - 6 = 0")
coeffs_c = [2.0, 9.0, 0.0, -6.0]
up_c = upper_bnd(coeffs_c)
dwn_c = lower_bnd(coeffs_c)
print(f"Bounds from Horner: [{dwn_c} : {up_c}]")
f_c = lambda x: 2 * x**3 + 9 * x**2 - 6
intervals_c = find_intervals(f_c, dwn_c, up_c, 0.1)
print(f"Bounds with roots: {intervals_c}\n")