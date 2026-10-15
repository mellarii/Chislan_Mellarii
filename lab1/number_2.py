  import math

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
      for i in c:
        i = i * (-1)
    
    L = 1
    while L <= 500:
      vals = horner(c, L)
      for v in vals:
        if all(v >= 0):
          return L
      L += 1
    return None

  # Находит нижнюю границу отрицательных корней.
  # Меняем знаки у коэффициентов при нечетных степенях.
  # len(coeffs)-1 - i дает степень текущего коэффициента.
  # Если степень нечетная, (-1)**степень = -1, знак меняется.
  def lower_bnd(coeffs):
    for i in range(len(coeffs)):
      c_neg = (coeffs[i] *((-1) ** (len(coeffs - 1 - i))))

    # Nfr ;t rfr d dth[ytq yj *-1]
    L = upper_bnd(c_neg)
    if L is not None:
      return -L
    return None

  # --- На моем варианте 52 --- #
  print("Uravneniye 1: 0.3x + 0.5^3 -1.2 = 0")
  coeffs_poly = [0.5, 0.0, 0.3, -1.2]
  up = upper_bnd(coeffs_poly)
  dwn = lower_bnd(coeffs_poly)

  print(f"Coeffs: {coeffs_poly}")
  print(f"Upper bound: {up}")
  print(f"Lower bound: {dwn}")
  print(f"Search interval: {dwn} - {up}")

