import numpy as np
import math

def modify_newton():
  print("Modify Newton method\n")

  def F(X): # Заданная система нелинейных уравнений 
    x, y = X[0], X[1]
    return np.array([
      math.sin(y + 1) - x - 1.2,
      2*y + math.cos(x) - 2
    ])

  def J(X): # Матрица якоби; В модНьютоне вычисляется только 1 раз 
    x, y = X[0], X[1]
    return np.array([
      [-1.0, math.cos(y + 1)],
      [-math.sin(x), 2.0]
    ])

  X0 = np.array([0.0,0.5])

  det_J = np.linalg.det(J(X0)) # Условие существования решения матрицы якоби !!! переделать счет дет вручную
  print(f"Opredelitel Yakobi matrix: {det_J:.4f}")
  if abs(det_J) < 1e-10:
    print("Error - Yakobi matrix &&&&&&& ???? Virozdena******ispravit' ya ne pomnu kak na angliyskom")
    return

  J_inv = np.linalg.inv(J(X0)) # Обратная матрица якоби !!! тоже без нумпи
  X = X0.copy()
  tol = 0.001
  max_iters = 50

  print(f"{'Iter':<5} | {'x':<10} | {'y':<10}")
  print("-" * 35)

  for i in range(max_iters):
    F_val = F(X) # Значение функции в шаге
    delta = -np.dot(J_inv, F_val) # Матричное умножение значение функции на обратную матрицу якоби
    X_new = X + delta # Итерационная формула
  
    if np.max(np.abs(X_new - X)) < tol:
      print("-" * 60)
      print(f"Result: x = {X_new[0]:.4f}, y = {X_new[1]:.4f}")

  X = X_new

# !! без нумпи

def gradient_method():
  print("\n--- Gradient method ---")
    
  def F1(x, y):
    return math.tan(x * y) - x**2

  def F2(x, y):
    return 7 * x**2 + 2 * y**2 - 1

  def S(x, y): # Целевая функция
    return F1(x, y)**2 + F2(x, y)**2

  def grad_S(x, y): # Вектор - градиет целевой функции для поиска минимума
    f1 = F1(x, y)
    f2 = F2(x, y)
    cos_sq = math.cos(x * y)**2
      
    df1_dx = y / cos_sq - 2 * x
    df1_dy = x / cos_sq
    df2_dx = 14 * x
    df2_dy = 4 * y
      
    ds_dx = 2 * f1 * df1_dx + 2 * f2 * df2_dx
    ds_dy = 2 * f1 * df1_dy + 2 * f2 * df2_dy

    return np.array([ds_dx, ds_dy])

  X = np.array([0.2, 0.6]) 
  tol = 0.001
  alpha = 0.05
  max_iter = 1000

  print(f"{'Iyeration':<8} | {'x':<10} | {'y':<10} | {'S(x,y)':<12} | {'Step':<12}")
  print("-" * 65)

  for i in range(max_iter):
    grad = grad_S(X[0], X[1])
        
    temp_alpha = alpha
    X_new = X - temp_alpha * grad # Итерационная функция градиентного спуска
      
    while S(X_new[0], X_new[1]) > S(X[0], X[1]) and temp_alpha > 1e-6: # Подбираем шаг спуска пока функцяи не начнет убывать
      temp_alpha /= 2
      X_new = X - temp_alpha * grad

    print(f"{i+1:<8} | {X_new[0]:.6f}   | {X_new[1]:.6f}   | {S(X_new[0], X_new[1]):.6f}   | {temp_alpha:.5f}")

    if np.max(np.abs(X_new - X)) < tol:
      print("-" * 65)
      print(f"Result: x = {X_new[0]:.4f}, y = {X_new[1]:.4f}")
      break
            
    X = X_new


if __name__ == "__main__":
  modify_newton()
  gradient_method()

# Словесная интерпритация методов как ребеночку маленькому объяснить
# ВЫбор начального приближения 