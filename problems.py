import random

from dataclasses import dataclass


@dataclass
class Problem:

    term: str
    solution: int
    options: tuple[int, int, int]


MINUS = '\u2212'
MULTIPLY = '\u00d7'
DIVIDE = '\u00f7'


def random_problems(n_problems_for_operator: tuple[int, int, int, int]) -> tuple[Problem, ...]:
    problems = []
    for _ in range(n_problems_for_operator[0]):
        problems.append(__random_problem('+'))
    for _ in range(n_problems_for_operator[1]):
        problems.append(__random_problem(MINUS))
    for _ in range(n_problems_for_operator[2]):
        problems.append(__random_problem(MULTIPLY))
    for _ in range(n_problems_for_operator[3]):
        problems.append(__random_problem(DIVIDE))
    random.shuffle(problems)
    return tuple(problems)


def __random_problem(op) -> Problem:
    op_to_func = {
        '+': __random_addition_problem,
        MINUS: __random_subtraction_problem,
        MULTIPLY: __random_multiplication_problem,
        DIVIDE: __random_division_problem,
    }
    func = op_to_func[op]
    (term, solution) = func()
    options = __random_options(solution)
    return Problem(term, solution, options)


def __random_addition_problem() -> tuple[str, int]:
    summand_1 = random.randint(0, 50)
    summand_2 = random.randint(0, 50)
    solution = summand_1 + summand_2
    return (f'{summand_1} + {summand_2}', solution)


def __random_subtraction_problem() -> tuple[str, int]:
    minuend = random.randint(0, 50)
    subtrahend = random.randint(0, minuend)
    solution = minuend - subtrahend
    return (f'{minuend} {MINUS} {subtrahend}', solution)


def __random_multiplication_problem() -> tuple[str, int]:
    factor_1 = random.randint(0, 10)
    factor_2 = random.randint(0, 10)
    solution = factor_1 * factor_2
    return (f'{factor_1} {MULTIPLY} {factor_2}', solution)


def __random_division_problem() -> tuple[str, int]:
    divisor = random.randint(1, 10)
    solution = random.randint(0, 10)
    dividend = divisor * solution
    return (f'{dividend} {DIVIDE} {divisor}', solution)


def __random_options(solution: int) -> tuple[int, int, int]:
    if solution == 0:
        option_2 = random.randint(1, 3)
        choices_for_option_3 = [1, 2, 3]
        choices_for_option_3.remove(option_2)
        option_3 = random.choice(choices_for_option_3)
        options = [0, option_2, option_3]
        options.sort()
        return tuple(options)
    if solution == 1:
        option_pattern = random.choice((2, 3, 3))
    else:
        option_pattern = random.randint(1, 3)
    match option_pattern:
        case 1: # zwei Optionen kleiner als die Lösung
            x = min(solution * 0.1, 0.7)
            d = int(solution * x)
            additional_options = random.sample(range(d, solution), 2)
            additional_options.sort()
            return (*additional_options, solution)
        case 2: # eine Option kleiner, eine Option größer als die Lösung
            x = min(solution * 0.2, 0.70)
            d = int(solution * x)
            p = 2 * solution - d
            option_1 = random.randint(d, solution - 1)
            option_3 = random.randint(solution + 1, p)
            return (option_1, solution, option_3)
        case 3: # zwei Optionen größer als die Lösung
            x = min(solution * 0.2, 0.7)
            d = int(solution * x)
            p = 2 * solution - d + 1
            additional_options = random.sample(range(solution + 1, p + 1), 2)
            additional_options.sort()
            return (solution, *additional_options)