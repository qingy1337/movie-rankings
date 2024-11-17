import os
import requests

try:
    import pyfiglet
except:
    print("Installing package pyfiglet...")
    os.system('pip install pyfiglet -q')
    print("Done installing pyfiglet\n\n")
    import pyfiglet

# Function to display welcome ASCII art
def ascii_art():
    print(pyfiglet.figlet_format("Welcome to MVR"))

# Function to handle login
def handle_login():
    username = input("Username: ")
    password = input("Password: ")
    return username, password

# Function to save token to file
def save_token(token,username):
    with open('.mvr_token', 'w') as f:
        f.write(f"{token}%{username}")

# Function to read token from file
def read_token():
    if os.path.exists('.mvr_token'):
        with open('.mvr_token', 'r') as f:
            return f.read().strip().split('%')
    return None, None

# Function to authenticate and get token
def authenticate(username, password):
    response = requests.get(f"https://albacore-powerful-racer.ngrok-free.app/login?username={username}&password={password}")
    if response.json().get('authorized'):
        token = response.json().get('token')
        return token
    return None

# Main function
def main():
    token, username = read_token()
    if not token:
        ascii_art()
        while True:
            username, password = handle_login()
            token = authenticate(username, password)
            if token:
                save_token(token, username)
                print("Successfully logged in!")
                print("\n" + "-" * 30 + "\n")
                break
            else:
                print("Login failed. Please try again.")
    else:
        print(pyfiglet.figlet_format("Welcome, "+username))

    while True:
        response = requests.get(f"https://albacore-powerful-racer.ngrok-free.app/take-two")
        movies = response.json()

        user_input = input(f"Which of these movies is better? [{movies['m1']}] or [{movies['m2']}]\nAnswer: ")
        if user_input.lower() == 'quit':
            break
        if user_input not in ['0', '1', '2']:
            print("Invalid input. Please enter 0 for a tie, 1 for the first movie, or 2 for the second movie.")
            continue

        requests.post("https://albacore-powerful-racer.ngrok-free.app/rank", params={
            "m1": movies['m1'],
            "m2": movies['m2'],
            "token": token,
            "choice": int(user_input),
        })

        print("Movie rankings updated!")
        print("\n" + "-" * 30 + "\n")

if __name__ == "__main__":
    main()