from enum import Enum


class OperationTypes(Enum):
    """
    Admin operations
        Operations on event:
        - add event
        - update event
        - approve event
        - archive event
        - unarchive event
        - delete event

        Operations on user:
        - add user
        - deactivate user
        - activate user
        - delete user

    Users opérations
        Operations on event:
        - participate
        - give note and review
    """

    ADDED_EVENT = 'added_event'
    UPDATED_EVENT = 'updated_event'
    APPROVED_EVENT = 'approved_event'
    ARCHIVED_EVENT = 'archived_event'
    UNARCHIVED_EVENT = 'unarchived_event'
    DELETED_EVENT = 'deleted_event'
    UPDATED_IMAGE = 'updated_image'
    ADDED_USER = 'added_user'
    ACTIVATED_USER = 'activated_user'
    DEACTIVATED_USER = 'deactivated_user'
    DELETED_USER = 'deleted_user'
