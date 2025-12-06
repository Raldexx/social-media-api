from passlib.context import CryptContext


# Password hashing context
# bcrypt algorithm with automatic salt generation
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """
    Password hashing and verification utilities
    """
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against hashed password
        
        Args:
            plain_password: User's input password (plain text)
            hashed_password: Stored hashed password from database
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a plain password
        
        Args:
            password: Plain text password to hash
            
        Returns:
            str: Hashed password string
        """
        return pwd_context.hash(password)