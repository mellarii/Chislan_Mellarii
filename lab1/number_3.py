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
  history = []
  while True:
    x = b - f(b) * (b - a) / (f(b) - f(a))
    iters+=1
    history.append((a, b, x))
    if abs(x - a) < eps:
      return x, iters, history
    a = x

# --- б) Метод Касаельных --- #

def start_point(f, d2f, a, b):
  # Выбираем точку из отрезка [a,b] для которой выполняется условие "f(x0) * f''(x0) > 0"
  if f(a) * d2f(a) > 0:
    return a
  elif f(b) * d2f(b) > 0:
    return b
  else:
    return (a + b)/2

def tangent_method(f, df, x0, eps=0.001):
  iters = 0
  history = []
  x_curr = x0
  while True:
    x_next = x_curr - f(x_curr) / df(x_curr)
    iters+=1
    history.append((x_curr, x_next))
    if abs(x_next - x_curr) < eps:
      return x_next, iters, history
    x_curr = x_next

# --- в) Комбинированный метод --- #

def combined_method(f, df, d2f, a, b, eps=0.001):
  iters = 0
  history = []
  while True:
    if f(a) * d2f(a) > 0:
      x_tan = a - f(a) / df(a)
      x_chord = b - f(b) * (b - a) / (f(b) - f(a))
      history.append((a, b, x_chord, x_tan, True)) 
      a, b = x_chord, x_tan
    else: 
      x_tan = b - f(b) / df(b)
      x_chord = a - f(a) * (b - a) / (f(b) - f(a))
      history.append((a, b, x_chord, x_tan, False)) 
      a, b = x_chord, x_tan
    iters+=1
    if abs(b - a) < eps:
      return (a + b)/2, iters, history

# === Сам третий номер === #

# --- Уравнение а) 2x-lg(x)-7=0 --- #
print("a) 2x - lg(x) - 7 = 0")
f_a = lambda x: 2 * x - math.log(x) - 7
# ОО x > 0 -> от 0.1 до 10
intervals_a = find_intervals(f_a, 0.1, 10, 0.1)
print(f"Bounds with roots: {intervals_a}")

a_a, b_a = intervals_a[0]
root_chord, iters_chord, history_chord = chord_method(f_a, a_a, b_a)
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

# Производные
df_b = lambda x: 3 * x**2 - 6 * x + 6
d2f_b = lambda x: 6 * x - 6

a_b, b_b = intervals_b[0]
x0_b = start_point(f_b, d2f_b, a_b, b_b)
print(f"Choosen start point for p. b): {x0_b}")

root_tangent, iters_tangent, history_tangent = tangent_method(f_b, df_b, x0_b)
print(f"Root (tangent method): {root_tangent}. \nIterations count: {iters_tangent}")

# --- Уравнение в) 2x^3+9x^2-6=0 --- #
print("\nc) 2x^3 + 9x^2 - 6 = 0")
coeffs_c = [2.0, 9.0, 0.0, -6.0]
up_c = upper_bnd(coeffs_c)
dwn_c = lower_bnd(coeffs_c)
print(f"Bounds from Horner: [{dwn_c} : {up_c}]")
f_c = lambda x: 2 * x**3 + 9 * x**2 - 6
intervals_c = find_intervals(f_c, dwn_c, up_c, 0.1)
print(f"Bounds with roots: {intervals_c}\n")

# Производные
df_c = lambda x: 6 * x**2 + 18 * x
d2f_c = lambda x: 12 * x + 18

a_c, b_c = intervals_c[0]
x0_c = start_point(f_c, d2f_c, a_c, b_c)
print(f"Choosen start point for p. c): {x0_c}")

root_combined, iters_combined, history_combined = combined_method(f_c, df_c, d2f_c, a_c, b_c)
print(f"Root (combined method): {root_combined}. \nIterations count: {iters_combined}")

# ==========================================
# Визуализация (Графическое отделение) <- Thank depseek
# ==========================================

def plot_chord(f, a, b, root, history, title):
    pad = 0.5 * (b - a)
    xs = [a - pad + (b - a + 2*pad) * i / 300 for i in range(301)]
    ys = [f(x) for x in xs]

    pl.figure(figsize=(9, 6))
    pl.plot(xs, ys, 'b-', label='f(x)', linewidth=2)
    pl.axhline(0, color='black', linewidth=0.8)

    n = len(history)
    for i, (pod, nepod, x_new) in enumerate(history):
        alpha = 0.3 + 0.7 * (i + 1) / n
        pl.plot([pod, nepod], [f(pod), f(nepod)], '--',
                color='orange', alpha=alpha, linewidth=1.8,
                label='Хорды' if i == 0 else None)
        pl.plot(x_new, 0, 'o', color='orange', alpha=alpha, markersize=6)

    pl.axvline(root, color='red', linestyle='--',
               label=f'Корень ≈ {root:.5f}')
    pl.plot(root, 0, 'ro', markersize=10)
    pl.title(title)
    pl.xlabel('x'); pl.ylabel('f(x)')
    pl.grid(True, alpha=0.3); pl.legend()
    pl.show()


def plot_tangent(f, df, a, b, root, history, title):
    pad = 0.5 * (b - a)
    xs = [a - pad + (b - a + 2*pad) * i / 300 for i in range(301)]
    ys = [f(x) for x in xs]

    pl.figure(figsize=(9, 6))
    pl.plot(xs, ys, 'b-', label='f(x)', linewidth=2)
    pl.axhline(0, color='black', linewidth=0.8)

    n = len(history)
    for i, (x_curr, x_next) in enumerate(history):
        alpha = 0.3 + 0.7 * (i + 1) / n
        pl.plot([x_curr, x_next], [f(x_curr), 0], '-',
                color='green', alpha=alpha, linewidth=1.8,
                label='Касательные' if i == 0 else None)
        pl.plot(x_next, 0, 'o', color='green', alpha=alpha, markersize=6)

    pl.axvline(root, color='red', linestyle='--',
               label=f'Корень ≈ {root:.5f}')
    pl.plot(root, 0, 'ro', markersize=10)
    pl.title(title)
    pl.xlabel('x'); pl.ylabel('f(x)')
    pl.grid(True, alpha=0.3); pl.legend()
    pl.show()


def plot_combined(f, a, b, root, history, title):
    pad = 0.5 * (b - a)
    xs = [a - pad + (b - a + 2*pad) * i / 300 for i in range(301)]
    ys = [f(x) for x in xs]

    pl.figure(figsize=(9, 6))
    pl.plot(xs, ys, 'b-', label='f(x)', linewidth=2)
    pl.axhline(0, color='black', linewidth=0.8)

    n = len(history)
    for i, (a_i, b_i, x_chord, x_tan, tan_from_a) in enumerate(history):
        alpha = 0.3 + 0.7 * (i + 1) / n
        # Хорда: от a_i до b_i
        pl.plot([a_i, b_i], [f(a_i), f(b_i)], '--',
                color='orange', alpha=alpha, linewidth=1.8,
                label='Хорды' if i == 0 else None)
        # Касательная: либо из a, либо из b
        x_start = a_i if tan_from_a else b_i
        pl.plot([x_start, x_tan], [f(x_start), 0], '-',
                color='green', alpha=alpha, linewidth=1.8,
                label='Касательные' if i == 0 else None)
        pl.plot(x_chord, 0, 'o', color='orange', alpha=alpha, markersize=6)
        pl.plot(x_tan, 0, 'o', color='green', alpha=alpha, markersize=6)

    pl.axvline(root, color='red', linestyle='--',
               label=f'Корень ≈ {root:.5f}')
    pl.plot(root, 0, 'ro', markersize=10)
    pl.title(title)
    pl.xlabel('x'); pl.ylabel('f(x)')
    pl.grid(True, alpha=0.3); pl.legend()
    pl.show()


# --- сам Вывод функций грффически --- #
plot_chord(f_a, a_a, b_a, root_chord, history_chord, "Chord method: ")
plot_tangent(f_b, df_b, a_b, b_b, root_tangent, history_tangent, "Tangent method: ")
plot_combined(f_c, a_c, b_c, root_combined, history_combined, "Combined method: ")
