class UserAlreadyExists(Exception):
    pass

class UserDoesNotExist(Exception):
    pass

class LoginBlocked(Exception):
    pass

class IncorrectPassword(Exception):
    pass

class InvalidToken(Exception):
    pass

class TokenExpired(Exception):
    pass