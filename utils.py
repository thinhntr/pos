from typing import List, Union

import readline


def lcs(s1, s2, len1, len2):
    if 0 in (len1, len2):
        return 0

    elif s1[len1 - 1] == s2[len2 - 1]:
        return 1 + lcs(s1, s2, len1 - 1, len2 - 1)

    else:
        return max(
            lcs(s1, s2, len1 - 1, len2),
            lcs(s1, s2, len1, len2 - 1)
        )


def dp_lcs(X, Y):
    m = len(X)
    n = len(Y)

    L = [[None]*(n+1) for i in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    return L[m][n]


def clrscr():
    print('\n' * 100)


def construct_choices(choices: List[Union[str, int]], contents: List[str]) -> List[List]:
    """
    Return a list of [choice, content] for each choices and contents
    """
    if len(choices) != len(contents):
        raise ValueError("len of choices and contents doesn't match")

    return [option for option in zip(choices, contents)]


def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def get_choice(options: List[List], title: str = "Choose one of these") -> Union[str, int, None]:
    print(title)

    valid_choices = ["c"]
    for option in options:
        print(f"    {option[0]}) {option[1]}")
        valid_choices.append(str(option[0]))
    print("    c) Cancel")

    choice = input("Your choice: ").strip()

    if choice == "c" or choice not in valid_choices:
        return None

    return int(choice) if choice.isnumeric() else choice
