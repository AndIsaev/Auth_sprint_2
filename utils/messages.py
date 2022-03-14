from . import constants

""" Password validation messages """
PASSWORD_UPPER_LATTER: str = "The password must contain UPPER case symbols"
PASSWORD_LOWER_LATTER: str = "The password must contain LOWER case symbols"
PASSWORD_MIN_LENGTH: str = (
    f"The password can't be less then {constants.PASSWORD_MIN_LENGTH} symbols"
)
PASSWORD_MAX_LENGTH: str = (
    f"The password must be less then {constants.PASSWORD_MAX_LENGTH} symbols"
)
PASSWORD_INTEGER_SYMBOL: str = "The password must contain numbers"
PASSWORD_ALPHABET: str = "Please, use only latin letters, numbers and signs '!#?.'"


""" Username validation messages """
USERNAME_FIRST_SYMBOL: str = (
    "The first character must be letter in UPPER case of the English alphabet"
)
USERNAME_OTHER_SYMBOLS: str = (
    "Username must consist of English alphabet, numbers or underscore '_'"
)
USERNAME_MIN_INVALID: str = (
    f"The username can't be less then {constants.USERNAME_MIN_LENGTH} symbols"
)
USERNAME_MAX_INVALID: str = (
    f"The username must be less then {constants.USERNAME_MAX_LENGTH} symbols"
)
