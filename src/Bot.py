class Bot:
    def __init__(self, username: str, password: str, email: str, token: str) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.token = token
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getToken(self):
        return self.token