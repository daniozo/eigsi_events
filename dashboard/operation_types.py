from enum import Enum


class OperationTypes(Enum):
    """ Operation Types """

    """ Event """
    ADDED_EVENT = 'added_event'
    UPDATED_EVENT = 'updated_event'
    APPROVED_EVENT = 'approved_event'
    ARCHIVED_EVENT = 'archived_event'
    UNARCHIVED_EVENT = 'unarchived_event'
    DELETED_EVENT = 'deleted_event'
    UPDATED_IMAGE = 'updated_image'

    """ Participation """
    REGISTERED = 'registered'
    REQUESTED_REGISTRATION = 'requested_registration'
    APPROVED_REGISTRATION = 'approved_registration'
    REJECTED_REGISTRATION = 'rejected_registration'
    CONFIRMED_PARTICIPATION = 'confirmed_participation'
    RECEIVED_RATING = 'received_rating'

    """ User """
    ADDED_USER = 'added_user'
    ACTIVATED_USER = 'activated_user'
    DEACTIVATED_USER = 'deactivated_user'
    DELETED_USER = 'deleted_user'
