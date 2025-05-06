from sympy import false, true

def check_simple(x: int) -> bool:
    for i in range(2, int(x / 2) + 1):
        if x % i == 0:
            return false

    return true

if __name__ == "__main__":
    numbers = 100
    counter = 0
    for i in range(1, numbers + 1):
        res = check_simple(i)
        counter += 1 if res == true else 0
        print(f"{i} {res}")

    print(f"in {numbers} numbers {counter} are simple")
