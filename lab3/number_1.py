import math

def modify_newton():
  print("Modify Newton method\n")

  def F(X):  # Заданная система нелинейных уравнений
    x, y = X[0], X[1]
    return [
      math.sin(y + 1) - x - 1.2,
      2 * y + math.cos(x) - 2
    ]

  def J(X):  # Матрица Якоби
    x, y = X[0], X[1]
    return [
      [-1.0, math.cos(y + 1)],
      [-math.sin(x), 2.0]
    ]

  X0 = [0.0, 0.5]

  # Определитель матрицы Якоби вручную
  J0 = J(X0)
  a, b = J0[0]
  c, d = J0[1]
  det_J = a * d - b * c

  print(f"Opredelitel Yakobi matrix: {det_J:.4f}")

  if abs(det_J) < 1e-10:
    print("Error - Yakobi matrix &&&&&&& ???? Virozdena******ispravit' ya ne pomnu kak na angliyskom")
    return

  # Обратная матрица Якоби 2x2 вручную
  J_inv = [
    [ d / det_J, -b / det_J],
    [-c / det_J,  a / det_J]
  ]

  X = X0.copy()
  tol = 0.001
  max_iters = 50

  print(f"{'Iter':<5} | {'x':<10} | {'y':<10}")
  print("-" * 35)

  for i in range(max_iters):
    F_val = F(X)

  # delta = -J_inv * F_val вручную
  delta0 = -(J_inv[0][0] * F_val[0] + J_inv[0][1] * F_val[1])
  delta1 = -(J_inv[1][0] * F_val[0] + J_inv[1][1] * F_val[1])

  X_new = [X[0] + delta0, X[1] + delta1]

  if max(abs(X_new[0] - X[0]), abs(X_new[1] - X[1])) < tol:
    print("-" * 60)
    print(f"Result: x = {X_new[0]:.4f}, y = {X_new[1]:.4f}")
    break

  X = X_new


def gradient_method():
  print("\n--- Gradient method ---")

  def F1(x, y):
    return math.tan(x * y) - x ** 2

  def F2(x, y):
    return 7 * x ** 2 + 2 * y ** 2 - 1

  def S(x, y):  # Целевая функция
    return F1(x, y) ** 2 + F2(x, y) ** 2

  def grad_S(x, y):  # Градиент целевой функции
    f1 = F1(x, y)
    f2 = F2(x, y)
    cos_sq = math.cos(x * y) ** 2

    df1_dx = y / cos_sq - 2 * x
    df1_dy = x / cos_sq
    df2_dx = 14 * x
    df2_dy = 4 * y

    ds_dx = 2 * f1 * df1_dx + 2 * f2 * df2_dx
    ds_dy = 2 * f1 * df1_dy + 2 * f2 * df2_dy

    return [ds_dx, ds_dy]

  X = [0.2, 0.6]
  tol = 0.001
  alpha = 0.05
  max_iter = 1000

  print(f"{'Iyeration':<8} | {'x':<10} | {'y':<10} | {'S(x,y)':<12} | {'Step':<12}")
  print("-" * 65)

  for i in range(max_iter):
    grad = grad_S(X[0], X[1])

    temp_alpha = alpha

    X_new = [
      X[0] - temp_alpha * grad[0],
      X[1] - temp_alpha * grad[1]
    ]

    # Подбор шага, пока функция не начнёт убывать
    while S(X_new[0], X_new[1]) > S(X[0], X[1]) and temp_alpha > 1e-6:
      temp_alpha /= 2
      X_new = [
        X[0] - temp_alpha * grad[0],
        X[1] - temp_alpha * grad[1]
      ]

      print(
        f"{i + 1:<8} | {X_new[0]:.6f}   | {X_new[1]:.6f}   | "
        f"{S(X_new[0], X_new[1]):.6f}   | {temp_alpha:.5f}"
      )

      if max(abs(X_new[0] - X[0]), abs(X_new[1] - X[1])) < tol:
          print("-" * 65)
          print(f"Result: x = {X_new[0]:.4f}, y = {X_new[1]:.4f}")
          break

      X = X_new

if __name__ == "__main__":
    modify_newton()
    gradient_method()