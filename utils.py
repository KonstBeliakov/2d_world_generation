import numba


@numba.njit(cache=True)
def dist(pos1, pos2) -> float:
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


if __name__ == '__main__':
    print(dist((0, 0), (1, 1)))
