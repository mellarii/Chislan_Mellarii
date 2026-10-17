import math
import matplotlib.pyplot as pl

# ======= P1 - bounds and Horner's Scheme ======= #

# Вычисляет значения полинома и его производных по схеме Горнера.
# Возвращает список b, где b[-1] = P(x), b[-2] = P'(x) и т.д.
def horner(coeffs, x):
  n = len(coeffs)
  b = [0.0] * n
  b[0] = coeffs[0]
  for i in range(1,n):
    b[i] = b[i-1] * x + coeffs[i]
  return b

# Находит верхнюю границу положительных корней по теореме Коши.
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

# Находит нижнюю границу отрицательных корней.
# Меняем знаки у коэффициентов при нечетных степенях.
# len(coeffs)-1 - i дает степень текущего коэффициента.
# Если степень нечетная, (-1)**степень = -1, знак меняется.
def lower_bnd(coeffs):
  c_neg = [coeffs[i] *((-1) ** (len(coeffs) - 1 - i)) for i in range(len(coeffs))]

  # Теперь ищем нижнюю границу для P(-x)
  L = upper_bnd(c_neg)
  if L is not None:
    return -L
  return None

# ======= P2 - Search roots with graphics ======= #

# Смотрим отрезок [a,b] с шагом в h
def find_intervals(f, a, b, h=0.1):
  x = a
  intervals = []
  while x < b:
    if f(x) * f(x + h) <=0:
      intervals.append((x,x+h))
    x += h
  return intervals

def itiration_method(phi, a, b, eps=0.001):
  x_curr = (a+b)/2
  iters = 0
  while True:
    x_next = phi(x_curr)
    iters += 1
    if abs(x_next - x_curr) < eps:
      return x_next, iters
    x_curr = x_next

# ===== Решение моего варианта 52 ===== #

# === Уравнение 1 === #
print("Uravneniye 1: 0.3x + 0.5x^3 -1.2 = 0")
coeffs_poly = [0.5, 0.0, 0.3, -1.2]
up = upper_bnd(coeffs_poly)
dwn = lower_bnd(coeffs_poly)
print(f"Bounds of roots: [{dwn} - {up}]")

# Функции полинома
f1 = lambda x: 0.5 * x**3 + 0.3 * x - 1.2
phi = lambda x: (2.4 - 0.6 * x) ** (1/3)

# Отрезок с корнями
intervals = find_intervals(f1, dwn, up, 0.1)
if intervals:
  root1, iter1 = itiration_method(phi, up, dwn)
print(f"Interval with bounds: {intervals}")


# === Тригонометрия второе уравнение == #

print("2x + cos(x) = 0.5")
# Это не полином это трига тут Горнера нельзя
# Если проверить подстановкой то понятно что корень между -1 ~ 0

f2 = lambda x: 2 * x + math.cos(x) - 0.5
phi2 = lambda x: (0.5 - math.cos(x))/2

intervals2 = find_intervals(f2, -1.0, 1.0, 0.1)
print(f"Interval with bounds: {intervals2}") 

if intervals2:
  a2, b2 = intervals2[0]
  root2, iters2 = itiration_method(phi2, a2, b2)
  print(f"Roots: x = {root2:.6f} (iterations = {iters2})")

# ==========================================
# Визуализация (Графическое отделение)
# ==========================================
def plot_graph(f, a, b, root, title):
    xs = [a + (b - a) * i / 200 for i in range(201)]
    ys = [f(x) for x in xs]
    
    pl.figure(figsize=(8, 5))
    pl.plot(xs, ys, label="f(x)", color="blue", linewidth=2)
    pl.axhline(0, color="black", linewidth=0.8)
    pl.axvline(root, color="red", linestyle="--", label=f"Корень ≈ {root:.4f}")
    pl.plot(root, 0, 'ro') # Красная точка на оси X
    pl.title(title)
    pl.xlabel("x")
    pl.ylabel("f(x)")
    pl.grid(True, linestyle="--", alpha=0.6)
    pl.legend()
    pl.show()

# Строим графики для обоих уравнений
plot_graph(f1, dwn, up, root1, "Уравнение 1: 0.5x³ + 0.3x - 1.2 = 0")
plot_graph(f2, -1.0, 1.0, root2, "Уравнение 2: 2x + cos(x) - 0.5 = 0")