
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


def search(s1, arr):
    s1 = s1.lower()

    if not isinstance(arr, list):
        arr = list(arr)

    indices_of_len = {}
    max_len = 0

    for i, s2 in enumerate(arr):
        current_len = dp_lcs(s1, s2.lower())
        max_len = max(max_len, current_len)
        try:
            indices_of_len[current_len].append(i)
        except KeyError:
            indices_of_len[current_len] = [i]

    names = []

    if max_len == 0:
        return names

    for i in indices_of_len[max_len]:
        names.append(arr[i])

    return names
