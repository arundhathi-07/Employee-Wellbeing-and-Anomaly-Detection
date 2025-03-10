import time
import datetime

# Dictionary to store session details
user_session = {}

def authenticate_user():
    """Authenticates the user and starts session tracking."""
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username == "admin" and password == "1234":
        print("Login successful!")
        user_session["username"] = username
        user_session["login_time"] = time.time()  # Store login timestamp
        return username
    else:
        print("Invalid credentials!")
        return None

def track_working_hours():
    """Calculates total working hours when the user logs out."""
    if "login_time" in user_session:
        logout_time = time.time()
        total_time = logout_time - user_session["login_time"]
        formatted_time = str(datetime.timedelta(seconds=int(total_time)))  # Format in HH:MM:SS
        print(f"Total working hours: {formatted_time}")
        return formatted_time
    else:
        print("Error: Login time not recorded.")
        return None

if __name__ == "__main__":
    user = authenticate_user()

    if user:
        input("Press Enter to log out...")  # Simulating user activity
        track_working_hours()  # Track total working hours upon logout

