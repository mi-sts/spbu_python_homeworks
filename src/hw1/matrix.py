from src.util.type_checking import is_number


class Matrix:
    def _check_elements_format(self, elements):
        if not isinstance(elements, (list, tuple)) or not all(isinstance(row, (list, tuple)) for row in elements):
            raise TypeError("A matrix elements should be in a two-dimensional array or tuple!")

        if not elements or not all(row for row in elements):
            raise TypeError("A matrix can't have empty rows or columns!")

        if not all(is_number(j) for i in elements for j in i):
            raise TypeError("A matrix should contain only int, float or complex elements!")

        row_length = len(elements[0])
        if not all(len(row) == row_length for row in elements):
            raise ValueError("A matrix rows should have an equal length!")

    def _have_same_dimensions(self, other):
        return self.height == other.height and self.width == other.width

    def __init__(self, elements):
        self._check_elements_format(elements)
        self.elements = elements
        self.height = len(elements)
        self.width = len(elements[0])

    def _check_index_format(self, index):
        if not isinstance(index, tuple) or len(index) != 2 or not all(isinstance(i, int) for i in index):
            raise ValueError("A matrix index should contain two int values!")

        if index[0] not in range(self.height) or index[1] not in range(self.width):
            raise IndexError("A matrix index is out of range!")

    def __getitem__(self, index):
        self._check_index_format(index)
        return self.elements[index[0]][index[1]]

    def __setitem__(self, index, value):
        self._check_index_format(index)
        if not is_number(value):
            raise TypeError("A matrix can contain only int, float or complex elements!")
        self.elements[index[0]][index[1]] = value

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("A matrix can only be summed with a matrix!")

        if not self._have_same_dimensions(other):
            raise ArithmeticError("Matrices should have same dimensions to be summed!")

        return Matrix([[self[i, j] + other[i, j] for j in range(self.width)] for i in range(self.height)])

    def __neg__(self):
        return Matrix([[-i for i in row] for row in self.elements])

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("A matrix can only be in a difference with a matrix!")

        if not self._have_same_dimensions(other):
            raise ArithmeticError("Matrices should have dimensions to be in a difference!")

        return self + (-other)

    def transposed(self):
        return Matrix([[self[j, i] for j in range(self.width)] for i in range(self.height)])

    def _multiply_matrix_by_number(self, matrix, number):
        return Matrix([[number * i for i in row] for row in matrix.elements])

    def __mul__(self, other):
        if is_number(other):
            return self._multiply_matrix_by_number(self, other)
        elif isinstance(other, Matrix):
            if self.width != other.height:
                raise ArithmeticError("Matrices are not the right size to be multiplied!")
            return Matrix(
                [
                    [sum([self[k, i] * other[i, j] for i in range(self.width)]) for j in range(other.width)]
                    for k in range(self.height)
                ]
            )
        else:
            raise TypeError("A matrix can only be multiplied by a number or another matrix!")

    def __rmul__(self, other):
        if not isinstance(other, Matrix):
            return self.__mul__(other)

    def __str__(self):
        return "|" + "|\n|".join(["".join(["{:4}".format(j) for j in i]) for i in self.elements]) + "|\n"
