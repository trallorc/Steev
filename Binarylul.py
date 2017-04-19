def dis(a):
    return 1 << a


def dis2(a, b):
    return (1 << a) + (1 << b)

def dis5(a,n):
    b = a>>n
    b = b<<n
    return b

def dis6(a,n):

    return a

def main():
    """print dis(int(raw_input("Enter lulda")))
    print dis2(int(raw_input("Enter hehe xd")), int(raw_input("Enter vapenation")))

    print dis5(int(raw_input("cuck")), int(raw_input("dank meme")))"""

    print dis6(int(raw_input('Enter hehe xd')), int(raw_input("Enter vapenation")))

if __name__ == '__main__':
    main()

