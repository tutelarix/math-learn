from enum import IntEnum
from pathlib import Path

from beaupy import select
from rich.console import Console

from math_testing_ops import multiplication_table


class MathOperations(IntEnum):
    Multiplication = 0
    Deletion = 1


def launch_app(cache_file_path, is_debug=False):
    console = Console(color_system="windows")
    console.clear()
    console.print("Привіт Вовчик! Давай потренуємо математику.")

    op_index = -1
    ops = ["Табличка множення", "Ділення", "Вихід"]
    while op_index != len(ops) - 1:
        console.print("Вибери з опцій нижче, що хочеш потренувати.")
        operation = select(ops, cursor="🢧", cursor_style="cyan")
        console.clear()
        console.print(f"Ти вибрав: {operation}.")

        op_index = ops.index(operation)
        if op_index == MathOperations.Multiplication:
            multiplication_table(cache_file_path, is_debug)
        elif op_index == MathOperations.Deletion:
            console.print("Ділення не реалізовано")

        console.print("")


def main():
    is_debug = True
    cache_file_path = Path(__file__).parent.joinpath("cache.dat")

    launch_app(cache_file_path, is_debug)


if __name__ == "__main__":
    main()
