"""
TruEditor - Submission Permissions
===================================
Custom permissions for submission access control.

Developer: Abdullah Dogan
"""

from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


def is_coauthor(user, submission):
    """Check if the user is a co-author (linked via Author.user) on this submission."""
    if not user or not user.is_authenticated:
        return False
    return submission.authors.filter(user=user).exists()


class IsOwnerOrCoAuthorReadOnly(permissions.BasePermission):
    """
    Owner can read and write.
    Co-authors (linked via Author.user) can read only.
    """

    def has_object_permission(self, request, view, obj):
        if obj.submitter == request.user:
            return True

        if request.method in permissions.SAFE_METHODS and is_coauthor(request.user, obj):
            return True

        return False


class CanEditSubmission(permissions.BasePermission):
    """
    Permission to check if submission can be edited.
    Only DRAFT and REVISION_REQUIRED submissions can be edited.
    Applies only to update/partial_update actions; custom actions
    (submit, withdraw, approve, build_pdf) handle their own validation.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Custom actions handle their own status validation
        if view.action not in ('update', 'partial_update'):
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
