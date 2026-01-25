class DomainException(Exception):
    """Exception de base pour le domaine"""
    pass

class UserNotFoundError(DomainException):
    pass

class DuplicateEmailError(DomainException):
    pass

class ValidationError(DomainException):
    pass