def main():
    n = str(get_int("Number: "))
    if card_validation(n):
        if n[0:2] in ["34", "37"] and len(n) == 15:
            print("AMEX")
        elif n[0:2] in ["51", "52", "53", "54", "55"] and len(n) == 16:
            print("MASTERCARD")
        elif n[0] == "4" and (len(n) == 13 or len(n) == 16):
            print("VISA")
        else:
            print("INVALID")


def get_int(message):
    while True:
        try:
            n = int(input(message))
            if n > 0:
                return n
        except ValueError:
            pass


def card_validation(number):
    validation = 0
    for i in number[-2::-2]:
        x = str(int(i) * 2)
        if len(x) > 1:
            validation += int(x[0]) + int(x[1])
            continue
        validation += int(x)

    for i in number[-1::-2]:
        validation += int(i)

    if str(validation)[-1] == "0":
        return True
    else:
        print("INVALID")
        return False


main()
