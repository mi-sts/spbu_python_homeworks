import math


class Vector:
    def _is_number(self, element):
        return isinstance(element, (int, float, complex))

    def __init__(self, first, *args):
        if not all(self._is_number(element) for element in args):
            raise TypeError("A vector can't have a non-numeric element!")

        self.elements = [first] + list(args)
        self.length = 1 + len(args)

    def __len__(self):
        return len(self.elements)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("A vector can only be summed with a vector!")

        if len(other) != len(self):
            raise ArithmeticError("Vectors in the sum have the different length!")

        return Vector(*[i + j for i, j in list(zip(self.elements, other.elements))])

    def __neg__(self):
        return Vector(*[-i for i in self.elements])

    def __sub__(self, other):
        if not (isinstance(other, Vector)):
            raise TypeError("A vector can only be in the difference with a vector!")

        if len(other) != len(self):
            raise ArithmeticError("Vectors in the difference have a different length!")

        return self + (-other)

    def module(self):
        return math.sqrt(sum([i * i for i in self.elements]))

    def __mul__(self, other):
        if self._is_number(other):
            return Vector(*[other * i for i in self.elements])
        elif isinstance(other, Vector):
            if other.length != self.length:
                raise ArithmeticError("Vectors in the multiplication have a different length!")

            return sum([i * j for i, j in list(zip(self.elements, other.elements))])  # Scalar product.

    def angle(self, other):
        if other.length != self.length:
            raise ArithmeticError("Can't find the angle between the vectors with a different length!")

        return math.acos((self * other) / (self.module() * other.module()))

    def __str__(self):
        return "(" + ", ".join([str(i) for i in self.elements]) + ")"

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False

        return self.elements == other.elements
