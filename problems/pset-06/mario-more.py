def main():
    height = get_int("Height: ")
    make_pyramid(height)


def get_int(message):
    while True:
        try:
            n = int(input(message))
            if n > 0 and n < 9:
                return n
        except ValueError:
            print("Not an integer")


def make_pyramid(number):
    for i in range(number):
        print(" " * (number - (i + 1)), end="")
        print("#" * (i + 1), end="")
        print("  ", end="")
        print("#" * (i + 1), end="")
        print()


main()
