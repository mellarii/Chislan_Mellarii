# ===                    Номер моего варианта - 58                       === #
# === Значит нужно разработать программу решения методом 1.3 - Халецкого === #

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

def halecky_cnt(A, b):
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

if __name__ == "__main__":
  A = [
      [ 3.0, -0.7,  0.6, -2.0],
      [ 2.0,  5.0, -1.0, -3.0],
      [-1.0,  2.0,  4.0,  1.0],
      [ 2.0,  1.0, -1.0,  5.0]
  ]
  b = [24.5, -1.5, -6.9, -8.6]

  x_exc = halecky_cnt(A, b)

  print("\n Answer: ")
  for i, val in enumerate(x_exc):
    print(f"x{i+1} = {val:.4f}")