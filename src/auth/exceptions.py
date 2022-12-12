from fastapi import HTTPException, status


def invalid_credentials_exception():
    """Return HTTPException 401 for invalid credentials"""
    response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )
    return response
