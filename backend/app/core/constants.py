"""Application constants."""
# File validation constants
ALLOWED_FILE_EXTENSIONS = {".pdf"}
MIN_TEXT_LENGTH = 50  # Minimum meaningful text length

# Error messages
ERROR_FILE_NOT_PDF = "File must be a PDF"
ERROR_FILE_TOO_LARGE = "File size exceeds {max_size}MB limit"
ERROR_NO_TEXT_EXTRACTED = "Could not extract meaningful text from PDF"
