import numpy as np

def strassen(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    #2冪の大きさのみ
    n = len(A) // 2
    if n == 0:
        return A * B
    a11, a12 = A[:n, :n], A[:n, n:]
    a21, a22 = A[n:, :n], A[n:, n:]
    b11, b12 = B[:n, :n], B[:n, n:]
    b21, b22 = B[n:, :n], B[n:, n:]
    P1 = strassen(a11 + a22, b11 + b22)
    P2 = strassen(a21 + a22, b11)
    P3 = strassen(a11, b12 - b22)
    P4 = strassen(a22, b21 - b11)
    P5 = strassen(a11 + a12, b22)
    P6 = strassen(a21 - a11, b11 + b12)
    P7 = strassen(a12 - a22, b21 + b22)
    return np.block([
        [P1 + P4 - P5 + P7, P3 + P5          ],
        [P2 + P4,           P1 - P2 + P3 + P6]
    ])