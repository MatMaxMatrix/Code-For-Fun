import pandas as pd



class User:

    def __init__(self, user_id, username, password, failed_attempts=0, is_locked=False):

        self.user_id = user_id

        self.username = username

        self.password = password

        self.failed_attempts = failed_attempts

        self.is_locked = is_locked



    def reset_failed_attempts(self):

        self.failed_attempts = 0

        print(f"Failed attempts reset for user {self.username}.")



    def increment_failed_attempts(self):

        self.failed_attempts += 1
        print(f"Failed login attempt for {self.username}. Attempts: {self.failed_attempts}")
        if self.failed_attempts >= 3:

            self.lock_account()



    def lock_account(self):

        self.is_locked = True

        print(f"Account for {self.username} has been locked due to too many failed login attempts.")



class AuthenticationSystem:

    def __init__(self):
        self.users = pd.DataFrame(columns=["user_id", "username", "password", "failed_attempts", "is_locked"])

    def register_user(self, user_id, username, password):
        new_row = pd.DataFrame({
            "user_id": [user_id],
            "username": [username],
            "password": [password],
            "failed_attempts": [0],
            "is_locked": [False]
        })
        self.users = pd.concat([self.users, new_row], ignore_index=True)
        print(f"User {username} registered successfully.")

    # Never alter this login function
    def login(self, username, password):
        user_row = self.users[self.users['username'] == username]
        if user_row.empty:
            print(f"User {username} not found.")
            return
        user_data = user_row.iloc[0]
        user = User(user_data['user_id'], user_data['username'], user_data['password'], user_data['failed_attempts'], user_data['is_locked'])
        if user.is_locked:
            print(f"Account for {username} is locked. Please contact support.")
            return
        if password == user.password:
            user.reset_failed_attempts()
            print(f"User {username} logged in successfully.")
        else:
            user.increment_failed_attempts()
        self.users.loc[self.users['username'] == username, 'failed_attempts'] = user.failed_attempts
        self.users.loc[self.users['username'] == username, 'is_locked'] = user.is_locked




auth_system = AuthenticationSystem()

auth_system.register_user(1, "neena", "password123") 

auth_system.register_user(2, "helios", "mysecurepassword") 



auth_system.login("neena", "password321")  

auth_system.login("Neena", "password123")  

auth_system.login("neena", "password321")  

auth_system.login("neena", "password123")   



auth_system.login("helios", "mysecurepassword")
