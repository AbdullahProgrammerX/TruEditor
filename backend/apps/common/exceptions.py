"""
TruEditor - Custom Exception Handler
====================================
Returns all API errors in a standardized format.

Developer: Abdullah Dogan
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler.
    
    Returns all errors in the following format:
    {
        "success": false,
        "error": {
            "code": "ERROR_CODE",
            "message": "Error message",
            "details": [...] // optional
        }
    }
    """
    # First, call DRF's default handler
    response = exception_handler(exc, context)
    
    if response is not None:
        # Determine error code
        error_code = get_error_code(exc, response.status_code)
        
        # Get error message
        error_message = get_error_message(response.data)
        
        # Get details (if any)
        error_details = get_error_details(response.data)
        
        # Standard error format
        custom_response = {
            'success': False,
            'error': {
                'code': error_code,
                'message': error_message,
            }
        }
        
        # Add details if available
        if error_details:
            custom_response['error']['details'] = error_details
        
        response.data = custom_response
    
    return response


def get_error_code(exc, status_code):
    """
    Return error code based on HTTP status code.
    """
    error_codes = {
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
        403: 'FORBIDDEN',
        404: 'NOT_FOUND',
        405: 'METHOD_NOT_ALLOWED',
        409: 'CONFLICT',
        422: 'VALIDATION_ERROR',
        429: 'RATE_LIMIT_EXCEEDED',
        500: 'INTERNAL_SERVER_ERROR',
    }
    
    return error_codes.get(status_code, 'UNKNOWN_ERROR')


def get_error_message(data):
    """
    Extract message from error data.
    """
    if isinstance(data, dict):
        # Use 'detail' key if available
        if 'detail' in data:
            return str(data['detail'])
        
        # Use 'message' key if available
        if 'message' in data:
            return str(data['message'])
        
        # Use 'non_field_errors' if available
        if 'non_field_errors' in data:
            errors = data['non_field_errors']
            if isinstance(errors, list) and errors:
                return str(errors[0])
        
        # Return first error
        for key, value in data.items():
            if isinstance(value, list) and value:
                return f"{key}: {value[0]}"
            elif isinstance(value, str):
                return f"{key}: {value}"
    
    elif isinstance(data, list) and data:
        return str(data[0])
    
    elif isinstance(data, str):
        return data
    
    return 'An error occurred'


def get_error_details(data):
    """
    Extract validation error details.
    """
    if not isinstance(data, dict):
        return None
    
    # No details if 'detail' or 'message' exists
    if 'detail' in data or 'message' in data:
        return None
    
    details = []
    
    for field, errors in data.items():
        if field == 'non_field_errors':
            continue
            
        if isinstance(errors, list):
            for error in errors:
                details.append({
                    'field': field,
                    'message': str(error)
                })
        elif isinstance(errors, str):
            details.append({
                'field': field,
                'message': errors
            })
    
    return details if details else None


# ============================================
# CUSTOM EXCEPTION CLASSES
# ============================================

class TruEditorException(Exception):
    """
    TruEditor base exception class.
    """
    default_message = 'An error occurred'
    default_code = 'TRUEDITOR_ERROR'
    
    def __init__(self, message=None, code=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        super().__init__(self.message)


class ORCIDAuthenticationError(TruEditorException):
    """
    ORCID authentication error.
    """
    default_message = 'ORCID authentication failed'
    default_code = 'ORCID_AUTH_ERROR'


class FileUploadError(TruEditorException):
    """
    File upload error.
    """
    default_message = 'An error occurred while uploading the file'
    default_code = 'FILE_UPLOAD_ERROR'


class PDFGenerationError(TruEditorException):
    """
    PDF generation error.
    """
    default_message = 'An error occurred while generating the PDF'
    default_code = 'PDF_GENERATION_ERROR'


class InvalidStateTransitionError(TruEditorException):
    """
    Invalid state transition error.
    """
    default_message = 'This action cannot be performed in the current state'
    default_code = 'INVALID_STATE_TRANSITION'


class SubmissionValidationError(TruEditorException):
    """
    Submission validation error.
    """
    default_message = 'Submission validation failed'
    default_code = 'SUBMISSION_VALIDATION_ERROR'


class AuthorLimitExceededError(TruEditorException):
    """
    Author limit exceeded error.
    """
    default_message = 'Maximum number of authors exceeded'
    default_code = 'AUTHOR_LIMIT_EXCEEDED'


class FileSizeLimitExceededError(TruEditorException):
    """
    File size limit exceeded error.
    """
    default_message = 'File size exceeds the maximum allowed limit'
    default_code = 'FILE_SIZE_LIMIT_EXCEEDED'
