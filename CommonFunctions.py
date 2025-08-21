import os

# Admin Login
def Login(userName, Password, SecretCode):
    return userName == 'admin' and Password == 'admin' and SecretCode == 1234

# Create New User
def CreateUser(firstName, lastName, initialBalance):
    # Read current autonumber
    with open("autonumber.txt", "r") as file:
        autonumber = int(file.read())

    # Increment and save new autonumber
    autonumber += 1
    with open("autonumber.txt", "w") as file:
        file.write(str(autonumber))

    # Generate credentials
    userName = f"{firstName}{lastName}_{autonumber}"
    password = f"{lastName}_{autonumber}**"
    pin = 1234

    # Create user file
    with open(f"{autonumber}.txt", "w") as file:
        file.write(f"Account Number: {autonumber}\n")
        file.write(f"Name: {firstName} {lastName}\n")
        file.write(f"Username: {userName}\n")
        file.write(f"Password: {password}\n")
        file.write(f"Balance: {initialBalance}\n")
        file.write(f"Pin: {pin}\n")

    print(f"User created successfully!\nUsername: {userName}\nPassword: {password}")

# View User by Account Number
def viewUser(autonumber):
    try:
        with open(f"{autonumber}.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("Sorry, user does not exist.")

# Update User Details
def updateUserDetails(accountNumber, newName, newLastName, newPin, initialBalance):
    userName = f"{newName}{newLastName}_{accountNumber}"
    password = f"{newLastName}_{accountNumber}**"

    with open(f"{accountNumber}.txt", "w") as file:
        file.write(f"Account Number: {accountNumber}\n")
        file.write(f"Name: {newName} {newLastName}\n")
        file.write(f"Username: {userName}\n")
        file.write(f"Password: {password}\n")
        file.write(f"Balance: {initialBalance}\n")
        file.write(f"Pin: {newPin}\n")

    print("User details updated successfully.")

# Delete User
def deleteUser(autonumber):
    try:
        os.remove(f"{autonumber}.txt")
        print("User deleted successfully.")
    except FileNotFoundError:
        print("Sorry, user does not exist.")

# Find File by Username
def findUserFile(username):
    for filename in os.listdir():
        if filename.endswith(".txt") and filename != "autonumber.txt":
            with open(filename, "r") as file:
                lines = file.readlines()
                if username in lines[2]:
                    return filename
    return None

# View Account Details
def viewUserDetails(username):
    filename = findUserFile(username)
    if filename:
        with open(filename, "r") as file:
            print(file.read())
    else:
        print("User not found.")

# Check Balance
def checkBalance(username):
    filename = findUserFile(username)
    if filename:
        with open(filename, "r") as file:
            lines = file.readlines()
            balance = lines[4].split(":")[1].strip()
            print("Your balance is:", balance)
    else:
        print("User not found.")

# Withdraw Money
def withdrawMoney(username, amount):
    filename = findUserFile(username)
    if filename:
        with open(filename, "r") as file:
            lines = file.readlines()
            balance = int(lines[4].split(":")[1].strip())
            if balance < amount:
                print("Insufficient funds.")
                return
            new_balance = balance - amount
            lines[4] = f"Balance: {new_balance}\n"
        with open(filename, "w") as file:
            file.writelines(lines)
        print("Withdrawal successful. New balance:", new_balance)
    else:
        print("User not found.")

# Deposit Money
def depositMoney(username, amount):
    filename = findUserFile(username)
    if filename:
        with open(filename, "r") as file:
            lines = file.readlines()
            balance = int(lines[4].split(":")[1].strip())
            new_balance = balance + amount
            lines[4] = f"Balance: {new_balance}\n"
        with open(filename, "w") as file:
            file.writelines(lines)
        print("Deposit successful. New balance:", new_balance)
    else:
        print("User not found.")

# Transfer Money
def transferMoney(senderUsername, receiverUsername, amount):
    senderFile = findUserFile(senderUsername)
    receiverFile = findUserFile(receiverUsername)

    if not senderFile or not receiverFile:
        print("Sender or receiver not found.")
        return

    # Withdraw from sender
    with open(senderFile, "r") as file:
        senderLines = file.readlines()
        senderBalance = int(senderLines[4].split(":")[1].strip())
        if senderBalance < amount:
            print("Insufficient funds.")
            return
        senderLines[4] = f"Balance: {senderBalance - amount}\n"

    # Deposit to receiver
    with open(receiverFile, "r") as file:
        receiverLines = file.readlines()
        receiverBalance = int(receiverLines[4].split(":")[1].strip())
        receiverLines[4] = f"Balance: {receiverBalance + amount}\n"

    # Write back updated balances
    with open(senderFile, "w") as file:
        file.writelines(senderLines)
    with open(receiverFile, "w") as file:
        file.writelines(receiverLines)

    print("Transfer successful.")

# Change PIN
def changePin(username, newPin):
    filename = findUserFile(username)
    if filename:
        with open(filename, "r") as file:
            lines = file.readlines()
            lines[5] = f"Pin: {newPin}\n"
        with open(filename, "w") as file:
            file.writelines(lines)
        print("PIN changed successfully.")
    else:
        print("User not found.")