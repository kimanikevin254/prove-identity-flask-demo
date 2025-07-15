class ProveAPIError(Exception):
    """Exception raised for Prove API errors"""
    pass


class AuthenticationError(Exception):
    """Exception raised for authentication errors"""
    pass


class ValidationError(Exception):
    """Exception raised for validation errors"""
    pass