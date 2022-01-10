def open_print(file):
    try:
        with open(file, 'r+') as f:
            lines = f.readlines()
            for line in lines:
                print(line.replace("\n", ""))
    except FileNotFoundError:
        print("No File Found")
        raise
    finally:
        print("Ended Execution")


open_print("Anime.txt")
