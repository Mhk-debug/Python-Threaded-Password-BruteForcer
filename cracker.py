password = ""
while password.strip() == "":
    password = input("Please enter a password: ")

with open("wordlist.txt", "r") as wordlist:
    passwordList = [r[:-1] for r in wordlist.readlines()]
    print(passwordList)