"""S-002: Prints a bcrypt hash to paste into .env
Imports: bcrypt
Exports: (script)
"""
import getpass
import bcrypt

pw = getpass.getpass("Password: ").encode()[:72]  # bcrypt ignores bytes past 72
print("AUTH_PASSWORD_HASH='" + bcrypt.hashpw(pw, bcrypt.gensalt()).decode() + "'")