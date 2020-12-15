from typing import Collection, Iterable, List, Sized, Tuple, Union

import readline


def lcs(s1: str, s2: str, len1: int, len2: int) -> int:
    """Longest Common Subsequence using recursive method"""
    if 0 in (len1, len2):
        return 0

    elif s1[len1 - 1] == s2[len2 - 1]:
        return 1 + lcs(s1, s2, len1 - 1, len2 - 1)

    else:
        return max(lcs(s1, s2, len1 - 1, len2), lcs(s1, s2, len1, len2 - 1))


def dp_lcs(X: str, Y: str):
    """Longest Common Subsequence implementation using dynamic programming"""
    m = len(X)
    n = len(Y)

    L: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                continue
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    return L[m][n]


def clrscr():
    """Clear terminal screen"""
    print("\n" * 100)


def is_not_valid_input(value: str) -> bool:
    """Return True if `value` is not valid to set to a product"""
    return " ".join(value.strip().split()) == ""


def to_valid_price(value: Union[str, int]) -> int:
    """Convert `value` to int type

    If `value` is a string then preprocess and convert it to int

    Raises
    ------
    RuntimeError
        If `value` can't be convert to a positive integer

    """
    if isinstance(value, str):
        value = value.replace(" ", "")
        if not value.isdecimal():
            raise RuntimeError(f"Can't convert{value} to int")
        value = int(value)

    return value


def construct_poll(
    choices: Collection[Union[str, int]], choices_values: Collection[str]
) -> List[Tuple[str, str]]:
    """Merges options and option_values into a list to create a poll

    Raises
    ------
    ValueError
        If len(options) != len(options_values)
    """
    if len(choices) != len(choices_values):
        raise ValueError("len of choices and contents doesn't match")

    return list(zip(map(str, choices), choices_values))


def get_choice(
    poll: Collection[Tuple[str, str]], title: str = "Choose one of these"
) -> Union[str, int, None]:
    """
    Create a poll and get user's choice


    """
    print(title)
    valid_choices = ["c"]

    for option in poll:
        print(f"    {option[0]}) {option[1]}")
        valid_choices.append(str(option[0]))
    print("    c) Cancel")

    choice = input("Your choice: ").strip()
    if choice == "c" or choice not in valid_choices:
        return None

    return int(choice) if choice.isnumeric() else choice


def rlinput(prompt: str, prefill: str = ""):
    """
    Read user's input. Default input is set with `prefill`
    """
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()