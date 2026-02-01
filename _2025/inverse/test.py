import numpy as np
from sympy import Matrix,pprint,BlockMatrix,GramSchmidt,symbols
import sympy
import scipy
from IPython import embed
class numpyuseful:
    @staticmethod
    def inv(arr):
        return np.linalg.inv(arr)
    @staticmethod
    def pinv(arr):
        pinv=np.linalg.pinv(arr)
        return pinv
    @staticmethod
    def rank(arr):
        return np.linalg.matrix_rank(arr)
    @staticmethod
    def det(arr):
        det=np.linalg.det(arr)
        return np.round(det,10) # here
    @staticmethod
    def eigen(arr):
        eigenvalues, eigenvectors = np.linalg.eig(arr)
        return eigenvalues, eigenvectors
    @staticmethod
    def svd(arr):
        U, S, Vt = np.linalg.svd(arr)
        return U, np.diag(S), Vt # here
class sympyuseful:
    @staticmethod
    def inv(arr):
        matrix=Matrix(arr)
        return matrix.inv()
    @staticmethod
    def pinv(arr):
        matrix=Matrix(arr)
        return matrix.pinv()
    @staticmethod
    def rref(arr):
        matrix=Matrix(arr)
        return matrix.rref(pivots=False)
    @staticmethod
    def rank(arr):
        matrix=Matrix(arr)
        return matrix.rank()
    @staticmethod
    def det(arr):
        matrix=Matrix(arr)
        return matrix.det()
    @staticmethod
    def svd(arr):
        matrix=Matrix(arr)
        U, S, V = matrix.singular_value_decomposition()
        return U, S, V.T # here
    @staticmethod
    def lu(arr):
        # P A = L U
        # SymPy 像是个老实的数学家，不到万不得已不换行
        matrix=Matrix(arr)
        L, U, p = matrix.LUdecomposition()
        P = sympy.eye(matrix.rows).permute_rows(p)
        return P,L,U
    @staticmethod
    def BlockColumns(columns):
        basis_matrix=BlockMatrix(columns).as_explicit()
        return basis_matrix

    @staticmethod
    def get_rowspace_basis(arr):
        matrix = Matrix(arr)
        # rowspace 返回行向量，需转置 (Transpose)
        basis = [v.T for v in matrix.rowspace()]
        return basis

    @staticmethod
    def get_columnspace_basis(arr):
        matrix = Matrix(arr)
        basis = matrix.columnspace()
        return basis

    @staticmethod
    def get_nullspace_basis(arr):
        matrix = Matrix(arr)
        basis = matrix.nullspace()
        return basis

    @staticmethod
    def get_leftnullspace_basis(arr):
        matrix = Matrix(arr)
        basis = matrix.T.nullspace()
        return basis

    @staticmethod
    def GramSchmidt(cols,orthonormal=False):
        return GramSchmidt(cols,orthonormal=orthonormal)

    @staticmethod
    def get_column_norm(arr):
        matrix = Matrix(arr)
        norms=[]
        for n in range(matrix.cols):
            norms.append(matrix.col(n).norm())
        return Matrix([norms])

class scipyuseful:
    @staticmethod
    def lu(arr):
        # A = P L U
        # SciPy 像是个精明的工程师，为了计算稳定，每一轮都要挑个最大的数当老大
        P, L, U = scipy.linalg.lu(arr)
        return P, L, U



if __name__ == '__main__':
    height=1080
    dst=10
    dmrate=0.25
    fontsize=60
    margin_h=10
    pixel=((height - dst) * dmrate) / (fontsize + margin_h)
    print(pixel)
    print(int(pixel))