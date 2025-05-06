def sum_of_2(targ: int, num: list[int]) -> list[int]:
    for i in range(len(num)):
        for j in range(i + 1, len(num)):
            if num[i] + num[j] == targ:
                return [i,j]
    return []

if __name__ == '__main__':
    num = [2, 7, 11, 13, 44]
    print(sum_of_2(9, num))

    num = [3, 2, 4]
    print(sum_of_2(6, num))

    num = [3, 3]
    print(sum_of_2(6, num))

    num = [3, 3, 2, 66, 5, 8]
    print(sum_of_2(9, num))