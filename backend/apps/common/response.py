"""
TruEditor - Response Helpers
============================
Helper functions for standardized API responses.

Developer: Abdullah Dogan
"""

from rest_framework.response import Response
from rest_framework import status as http_status


def success_response(data=None, message='Success', status_code=http_status.HTTP_200_OK):
    """
    Create a standardized success response.
    
    Args:
        data: Response data (dict, list, or None)
        message: Success message
        status_code: HTTP status code (default: 200)
    
    Returns:
        Response: DRF Response object
    
    Example:
        return success_response(
            data={'user': user_data},
            message='Profile updated successfully'
        )
    """
    response_data = {
        'success': True,
        'message': str(message),
    }
    
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)


def error_response(message, code='ERROR', details=None, status_code=http_status.HTTP_400_BAD_REQUEST):
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        code: Error code (e.g., 'VALIDATION_ERROR', 'NOT_FOUND')
        details: Additional error details (list or dict)
        status_code: HTTP status code (default: 400)
    
    Returns:
        Response: DRF Response object
    
    Example:
        return error_response(
            message='Validation failed',
            code='VALIDATION_ERROR',
            details=[{'field': 'email', 'message': 'Invalid email'}],
            status_code=400
        )
    """
    response_data = {
        'success': False,
        'error': {
            'code': code,
            'message': str(message),
        }
    }
    
    if details is not None:
        response_data['error']['details'] = details
    
    return Response(response_data, status=status_code)


def created_response(data=None, message='Created successfully'):
    """
    Shortcut for 201 Created response.
    """
    return success_response(
        data=data,
        message=message,
        status_code=http_status.HTTP_201_CREATED
    )


def no_content_response():
    """
    Shortcut for 204 No Content response.
    """
    return Response(status=http_status.HTTP_204_NO_CONTENT)


def not_found_response(message='Resource not found'):
    """
    Shortcut for 404 Not Found response.
    """
    return error_response(
        message=message,
        code='NOT_FOUND',
        status_code=http_status.HTTP_404_NOT_FOUND
    )


def unauthorized_response(message='Authentication required'):
    """
    Shortcut for 401 Unauthorized response.
    """
    return error_response(
        message=message,
        code='UNAUTHORIZED',
        status_code=http_status.HTTP_401_UNAUTHORIZED
    )


def forbidden_response(message='Permission denied'):
    """
    Shortcut for 403 Forbidden response.
    """
    return error_response(
        message=message,
        code='FORBIDDEN',
        status_code=http_status.HTTP_403_FORBIDDEN
    )


def validation_error_response(message='Validation error', details=None):
    """
    Shortcut for validation error response.
    """
    return error_response(
        message=message,
        code='VALIDATION_ERROR',
        details=details,
        status_code=http_status.HTTP_400_BAD_REQUEST
    )
