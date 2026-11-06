import numpy as np
import math

def modify_newton():
  print("Modify Newton method\n")

  def F(X):
    x, y = X[0], X[1]
    return np.array([
      math.sin(y + 1) - x - 1.2,
      2*y + math.cos(x) - 2
    ])

  def J(X):
    x, y = X[0], X[1]
    return np.array([
      [-1.0, math.cos(y + 1)],
      [-math.sin(x), 2.0]
    ])

  X0 = np.array([0.0,0.5])

  det_J = np.linalg.det(J(X0))
  print("Opredelitel Yakobi matrix: {det_J:.4f}")
  if abs(det_J) < 1e-10:
    print("Error - Yakobi matrix &&&&&&& ???? Virozdena******ispravit' ya ne pomnu kak na angliyskom")
    return 1

  J_inv = np.linalg.inv(J(X0))
  X = X0.copy()
  tol = 0.001
  max_iters = 50

  for i in range(max_iters):
    F_val = F(X)
    delta = -np.dot(J_inv, F_val)
    X_new = X + delta
  
  if np.max(np.abs(X_new - X)) < tol:
    print("-" * 60)
    print(f"x = {X_new[0]:.4f}, y = {X_new[1]:.4f}")

  X = X_new

if __name__ == "__main__":
  modify_newton()