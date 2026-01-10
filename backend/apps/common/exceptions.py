"""
TruEditor - Özel Exception Handler
==================================
Tüm API hatalarını standart formatta döner.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Özel exception handler.
    
    Tüm hataları aşağıdaki formatta döner:
    {
        "success": false,
        "error": {
            "code": "ERROR_CODE",
            "message": "Hata mesajı",
            "details": [...] // opsiyonel
        }
    }
    """
    # Önce DRF'nin varsayılan handler'ını çağır
    response = exception_handler(exc, context)
    
    if response is not None:
        # Hata kodunu belirle
        error_code = get_error_code(exc, response.status_code)
        
        # Hata mesajını al
        error_message = get_error_message(response.data)
        
        # Detayları al (varsa)
        error_details = get_error_details(response.data)
        
        # Standart hata formatı
        custom_response = {
            'success': False,
            'error': {
                'code': error_code,
                'message': error_message,
            }
        }
        
        # Detayları ekle (varsa)
        if error_details:
            custom_response['error']['details'] = error_details
        
        response.data = custom_response
    
    return response


def get_error_code(exc, status_code):
    """
    HTTP status koduna göre hata kodu döner.
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
    Hata verisinden mesaj çıkarır.
    """
    if isinstance(data, dict):
        # 'detail' anahtarı varsa kullan
        if 'detail' in data:
            return str(data['detail'])
        
        # 'message' anahtarı varsa kullan
        if 'message' in data:
            return str(data['message'])
        
        # 'non_field_errors' varsa kullan
        if 'non_field_errors' in data:
            errors = data['non_field_errors']
            if isinstance(errors, list) and errors:
                return str(errors[0])
        
        # İlk hatayı döndür
        for key, value in data.items():
            if isinstance(value, list) and value:
                return f"{key}: {value[0]}"
            elif isinstance(value, str):
                return f"{key}: {value}"
    
    elif isinstance(data, list) and data:
        return str(data[0])
    
    elif isinstance(data, str):
        return data
    
    return 'Bir hata oluştu'


def get_error_details(data):
    """
    Validasyon hatalarının detaylarını çıkarır.
    """
    if not isinstance(data, dict):
        return None
    
    # 'detail' veya 'message' varsa detay yok
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
# ÖZEL EXCEPTION SINIFLARI
# ============================================

class TruEditorException(Exception):
    """
    TruEditor temel exception sınıfı.
    """
    default_message = 'Bir hata oluştu'
    default_code = 'TRUEDITOR_ERROR'
    
    def __init__(self, message=None, code=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        super().__init__(self.message)


class ORCIDAuthenticationError(TruEditorException):
    """
    ORCID kimlik doğrulama hatası.
    """
    default_message = 'ORCID kimlik doğrulama başarısız'
    default_code = 'ORCID_AUTH_ERROR'


class FileUploadError(TruEditorException):
    """
    Dosya yükleme hatası.
    """
    default_message = 'Dosya yüklenirken bir hata oluştu'
    default_code = 'FILE_UPLOAD_ERROR'


class PDFGenerationError(TruEditorException):
    """
    PDF oluşturma hatası.
    """
    default_message = 'PDF oluşturulurken bir hata oluştu'
    default_code = 'PDF_GENERATION_ERROR'


class InvalidStateTransitionError(TruEditorException):
    """
    Geçersiz durum geçişi hatası.
    """
    default_message = 'Bu işlem mevcut durumda yapılamaz'
    default_code = 'INVALID_STATE_TRANSITION'
