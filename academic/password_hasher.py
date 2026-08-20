from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain_password: str) -> str:
  
    if not plain_password or not plain_password.strip():
        raise ValueError("La contraseña no puede estar vacía")
    return generate_password_hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
 
    if not plain_password or not hashed_password:
        return False
    return check_password_hash(hashed_password, plain_password)
