def get_greeting(name):
    return f"Hello {name}! Welcome to my software development portfolio."

def main():
    name = input("Please enter your name: ")
    print(get_greeting(name))

if __name__ == "__main__":
    main() 