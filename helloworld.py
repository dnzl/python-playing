import sqlite3

connection = sqlite3.connect('test.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL,
              birthdate DATE)''')
connection.commit()


def userExists(username):
    cursor.execute("SELECT id FROM users WHERE username = ?", [username])
    user = cursor.fetchone()
    return user is not None


def createUser(username, password, birthdate):
    cursor.execute("INSERT INTO users \
    (username, password, birthdate) VALUES \
    (?, ?, ?)", (username, password, birthdate))
    connection.commit()
    return cursor.lastrowid


def getUser(username, password):
    cursor.execute(
        "SELECT id, username, birthdate FROM users WHERE username = ? AND password = ?",
        [username, password]
    )
    return cursor.fetchone()


def showUsers():
    cursor.execute("SELECT id, username, birthdate FROM users")
    users = cursor.fetchall()
    for user in users:
        birthdate = user[2]
        if birthdate == "":
            birthdate = "None provided"

        print(
            "Id:", user[0],
            "| Username:", user[1],
            "| Birthdate:", birthdate
        )
    goNext()


def promptSignup():
    username = input('Insert a Username: ')
    if (userExists(username)):
        if (input("Username already exists. Wanna log in? (y/n) ") == 'y'):
            promptLogin()
        else:
            end()
            return

    password = input('Insert a Password: ')
    birthdate = input('Insert your Birthdate (YYYY-MM-DD): ')
    newId = createUser(username, password, birthdate)
    if (newId):
        print("Your account has been created! Your ID is: ", newId)
        goNext()
        return
    else:
        print("Oh no! something went wrong while creating your account :(")
        if (input('Do you want to start again? (y/n) ') == 'y'):
            start()
        else:
            end()
        return


def promptLogin():
    username = input('Username: ')
    if not userExists(username):
        if input("Username not found. Do you want to create a new user? (y/n) ") == 'y':
            promptSignup()
            return
        else:
            end()
            return

    password = input('Password: ')
    user = getUser(username, password)
    if (user is not None):
        if user[2] is None:
            birthdateString = "and your birthdate is: " + user[2]
        else:
            birthdateString = "and you didn't provide a birthdate"
        print(
            "Welcome back %s!" % user[1],
            "Your id is:", user[0],
            birthdateString
        )
    else:
        print("Oh no! something went wrong with those credentials :(")
        if (input('Do you want to start again? (y/n) ') == 'y'):
            start()
        else:
            end()
            return


def goNext():
    print("That was fun! Bye!")


def end():
    print("Alright then, bye!")


def start():
    print("Insert 1 to log in")
    print("Insert 2 to create a new user")
    print("Insert 3 to see a list of existent users")
    print("Insert q to quit")

    selection = input('Your option: ')

    if selection == '1':
        promptLogin()
    elif selection == '2':
        promptSignup()
    elif selection == '3':
        showUsers()
    elif selection == 'q':
        end()
    else:
        if input("I'm sorry, I didn't quite get that, would you try again? (y/n) ") == "y":
            start()
        else:
            end()


print("Hello there!")
start()

connection.close()
