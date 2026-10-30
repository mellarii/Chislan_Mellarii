import time

# ============================================ #
# === Сначала cntrl + c -> cntrl+v номер 1 === #
# ============================================ #

def halecky_decomp(A):
  n = len(A)
  L = [[0.0] * n for _ in range(n)]
  U = [[0.0] * n for _ in range(n)]
  for i in range(n):
    L[i][i] = 1.0
  
  for j in range(n):
    U[0][j] = A[0][j]
  for i in range(1,n):
    L[i][0] = A[i][0] / U[0][0]

  for k in range(1, n):
    for j in range(k, n):
      sum_u = sum(L[k][m] * U[m][j] for m in range(k))
      U[k][j] = A[k][j] - sum_u
  
    for i in range(k+1, n):
      sum_l = sum(L[i][m] * U[m][k] for m in range(k))
      L[i][k] = (A[i][k] - sum_l) / U[k][k]
  
  return L, U

def forward_sub(L, b):
  n = len(b)
  y = [0.0] * n
  for i in range(n):
    sum_y = sum(L[i][j] * y[j] for j in range(i))
    y[i] = b[i] - sum_y
  return y

def backwrd_sub(U, y):
  n = len(y)
  x = [0.0] * n
  for i in range(n - 1, -1, -1):
    sum_x = sum(U[i][j] * x[j] for j in range(i + 1, n))
    x[i] = (y[i] - sum_x) / U[i][i] 
  return x

def halecky_solve(A, b):
  print(" Solution by Halecky method \n")
  L, U = halecky_decomp(A)

  print("\n Matrix L (lower trngl): \n")
  for row in L:
    print([round(val, 4) for val in row])

  print("\n Matrix L (upper trngl): \n")
  for row in U:
    print([round(val, 4) for val in row])

  y = forward_sub(L, b)
  x = backwrd_sub(U, y)

  return x

# ============================================ #
# ===  Потом cntrl + c -> cntrl+v номер 2  === #
# ============================================ #

def iterForm_transform(A, b):
  n = len(A)
  C = [[0.0] * n for _ in range(n)]
  d = [0.0] * n

  for i in range(n):
    d[i] = b[i] / A[i][i]
    for j in range(n):
      if i != j:
        C[i][j] = -A[i][j] / A[i][i]

  return C, d

def iter_solve(A, b, eps=1e-4, max_iters=1000):
  print("\n Solution by iter-n method: \n")
  n = len(b)
  C, d = iterForm_transform(A, b)

  x_old = [0.0] * n
  x_new = [0.0] * n

  iters_cnt = 0
  err_history = []

  for k in range(max_iters):
    iters_cnt += 1

    for i in range(n):
      sum_cx = sum(C[i][j] * x_old[j] for j in range(n))
      x_new[i ] = d[i] +sum_cx

    max_diff = max(abs(x_new[i] - x_old[i]) for i in range(n))
    err_history.append(max_diff)

    if max_diff < eps:
      print(f"Reached {eps} for {iters_cnt} iterations")
      return x_new, iters_cnt, C

    x_old = x_new.copy()

  print(f"Reached max for {max_iters} iterations")
  return x_new, iters_cnt, C

# ============================================ #
# ===  Теперь реализация самого номера 3   === #
# ============================================ #

def check_convergence(C):
  n = len(C)
  norm = []
  for i in range(n):
    rows_sum = sum(abs(C[i][j]) for j in range(n))
    norm.append(rows_sum)
  max_norm = max(norm)

  print(f"Norm of matrix C: {max_norm}\n")
  if max_norm < 1:
    print("Since the norm < 1, the iterative process CONVERGES\n")
  else:
    print("Since the norm > 1, the iterative process NOT CONVERGES")

  return max_norm

if __name__ == "__main__":
  A = [
      [ 3.0, -0.7,  0.6, -2.0],
      [ 2.0,  5.0, -1.0, -3.0],
      [-1.0,  2.0,  4.0,  1.0],
      [ 2.0,  1.0, -1.0,  5.0]
  ]
  b = [24.5, -1.5, -6.9, -8.6]
  eps = 1e-4

  start_t = time.perf_counter()
  x_exact = halecky_solve(A, b)
  time_halecky = time.perf_counter() - start_t  

  start_t = time.perf_counter()
  x_app, iters, C_matrx = iter_solve(A, b, eps)
  time_app = time.perf_counter() - start_t  

  print("\nHalecky Answer\n")
  for i in range(len(x_exact)):
    print(f"x{i+1} = {x_exact[i]:.5f}")

  print("\nIterations Answer\n")
  for i in range(len(x_app)):
    print(f"x{i+1} = {x_app[i]:.5f}")

  max_err = max(abs(x_exact[i] - x_app[i]) for i in range(len(x_exact)))
  print(f"\nMax Error: {max_err:.6f}\n")

  print(f"\nTime for halecky: {time_halecky:.6f}\n")
  print(f"\nTime for iterations: {time_halecky:.6f}\n")

  check_convergence(C_matrx)
    