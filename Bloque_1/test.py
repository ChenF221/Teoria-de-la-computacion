
def ending_in_ing(word):
    if word is None or len(word) < 3:
        return 0
    if word[-3:] == "ing":
        return 1
    return 0


def read_file(path):
    count = 0
    with open(path, "r") as file:
        text = file.read()
        words = text.split()
        for word in words:
            count += ending_in_ing(word)
    return count
    

def main():
    num = read_file("Bloque_1//text_ing.txt")
    print(num)


if __name__ == "__main__":
    main()