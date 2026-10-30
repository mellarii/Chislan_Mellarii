# ===                    Номер моего варианта - 58                      === #
# === Значит нужно разработать программу решения методом 2.1 - Итерации === #

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
      return x_new, iters_cnt, err_history

    x_old = x_new.copy()

  print(f"Reached max for {max_iters} iterations")
  return x_new, iters_cnt, err_history

if __name__ == "__main__":
  A = [
      [ 3.0, -0.7,  0.6, -2.0],
      [ 2.0,  5.0, -1.0, -3.0],
      [-1.0,  2.0,  4.0,  1.0],
      [ 2.0,  1.0, -1.0,  5.0]
  ]
  b = [24.5, -1.5, -6.9, -8.6]

  x_app, iters, errors = iter_solve(A, b, eps=1e-4)

  print("\n Answer \n")
  for i, val in enumerate(x_app):
    print(f"x{i+1} = {val:.4f}")