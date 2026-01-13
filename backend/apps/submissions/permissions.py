"""
TruEditor - Submission Permissions
===================================
Custom permissions for submission access control.

Developer: Abdullah Dogan
"""

from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only submission owner to edit.
    Others can only read.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only to the owner
        return obj.submitter == request.user


class CanEditSubmission(permissions.BasePermission):
    """
    Permission to check if submission can be edited.
    Only DRAFT and REVISION_REQUIRED submissions can be edited.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only owner can edit
        if obj.submitter != request.user:
            return False
        
        # Only editable statuses
        return obj.is_editable


class CanDeleteSubmission(permissions.BasePermission):
    """
    Permission to check if submission can be deleted.
    Only DRAFT submissions can be deleted.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True
        
        # Only owner can delete
        if obj.submitter != request.user:
            return False
        
        # Only DRAFT can be deleted
        return obj.status == obj.Status.DRAFT
