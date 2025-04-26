"""modulo de validação de cpf"""

from random import randint

from locale import normalize
from re import sub as regex_substitute
from typing import Any


class CPF:
    """Classe de validação de CPF"""

    CPF_SIZE = 11
    STOP_CHARS = r"[^0-9]"
    DIVISOR = 11
    CPF_WEIGHTS = ((10, 9, 8, 7, 6, 5, 4, 3, 2), (11, 10, 9, 8, 7, 6, 5, 4, 3, 2))

    def __init__(self, cpf: str | int | None):
        self.cpf = CPF.normalize(str(cpf or ""))

    def __str__(self) -> str:
        """Retorna uma representação 'real', ou seja:
        eval(repr(cpf)) == cpf
        """
        return self.__cpf

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:
        eval(repr(cpf)) == cpf
        """
        return f"CPF('{self.__cpf}')"

    def __eq__(self, other: Any | None) -> bool:
        """
        Provê teste de igualdade para números de CPF
        """
        if not other:
            return False
        if isinstance(other, CPF):
            return self.cpf == other.cpf
        if isinstance(other, str):
            other = CPF.normalize(str)
            return self.cpf == other
        return False

    def is_valid(self, value: str | None = None) -> bool:
        """
        Valida o número de cpf
        """
        value = self.normalize(value or self.__cpf)
        source = CPF.__convert_to_list(self.cpf[:9])
        source.append(self.__gen(source))
        source.append(self.__gen(source))
        target = CPF.__convert_to_list(self.cpf)
        return source == target

    @staticmethod
    def __verify_sequence(value: str) -> str:
        if not value:
            raise ValueError("CPF could not be empty")
        sequence = value[0] * len(value)
        if sequence == value:
            msg = f"{value} could not be a sequence"
            raise ValueError(msg)
        return value

    @staticmethod
    def normalize(value: str) -> str:
        """normalize cpf"""
        if not value:
            raise ValueError("CPF could not be empty")
        value = regex_substitute(CPF.STOP_CHARS, "", value)
        value = value.zfill(CPF.CPF_SIZE)
        return CPF.__verify_sequence(value)

    @property
    def cpf(self) -> str:
        """CPF Getter"""
        return self.__cpf

    @cpf.setter
    def cpf(self, value: str | int):
        if not value:
            raise ValueError("CPF could not be empty")
        self.__cpf = normalize(str(value))

    @staticmethod
    def __convert_to_list(value: str) -> list[int]:
        """convert to list[int]"""
        if not value:
            raise ValueError("Invalid parameter")
        return [int(x) for x in value]

    @property
    def formatted(self) -> str:
        """CPF formatted Getter"""
        s = self.__cpf
        formatted = f"{s[:3]}.{s[3:6]}.{s[6:9]}-{s[9:]}"
        return formatted

    def __random_num(self):
        """generates a random number between 0 and 9"""
        return randint(0, 9)

    def __calculate_digit(self, cpf_list, factor):
        """
        The sum is calculated by multiplying each digit by a factor and summing the results
        If the sum is less than 2, the verifier digit is 0, otherwise it is 11 minus the
        remainder of the sum divided by 11
        """
        total_sum = sum([val * (factor - idx) for idx, val in enumerate(cpf_list)])
        return 0 if total_sum % 11 < 2 else 11 - (total_sum % 11)

    def generate(self) -> str:
        """
        Generates a list of 9 random numbers
        Calculates the first verifier digit
        Calculates the second verifier digit
        Returns the generated CPF as a string
        """
        # Generates a list of 9 random numbers
        cpf_list = [self.__random_num() for _ in range(9)]

        # Calculates the first verifier digit
        first_verifier = self.__calculate_digit(cpf_list, 10)
        cpf_list.append(first_verifier)

        # Calculates the second verifier digit
        second_verifier = self.__calculate_digit(cpf_list, 11)
        cpf_list.append(second_verifier)

        # Returns the generated CPF as a string
        return "".join(map(str, cpf_list))

    @staticmethod
    def __gen(value) -> int:
        """
        Gera o próximo dígito do número de CPF
        """
        res = []
        for i, a in enumerate(value):
            b = len(value) + 1 - i
            res.append(b * a)
        res = sum(res) % 11
        if res > 1:
            return 11 - res
        else:
            return 0


if __name__ == "__main__":
    cpf = CPF("59469390415")
    print(cpf.formatted)
    print(cpf)
    target: str = cpf
    print(f"Target: {target}")
    print(cpf.is_valid())
    cpf = CPF("012345")
    print(cpf.formatted)
    print(cpf)
    print(cpf.is_valid())
