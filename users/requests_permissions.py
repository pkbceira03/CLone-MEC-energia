from rest_framework import exceptions

from . import models

from utils.user_type_util import UserType

class RequestsPermissions:
    defaut_users_permissions = [
        UserType.super_user,
        UserType.university_user
    ]

    edit_users_permissions = [
        UserType.university_user
    ]

    def check_request_permissions(request_university_id, request_user, user_types_with_permission):
        user_type = UserType.get_user_type(request_user.type)

        user_has_permission = RequestsPermissions.check_user_has_permission(user_type, user_types_with_permission,
                                                                              request_university_id, request_user.id)
        
        if not user_has_permission:
            raise PermissionsException.user_has_not_permission_exception()

    def check_user_has_permission(user_type, user_types_with_permission, request_university_id, user_university_id):
        if user_type in user_types_with_permission:
            if user_type == UserType.university_user:
                return RequestsPermissions.check_university_user_permissions(request_university_id, user_university_id)

            return True

        return False

    def check_university_user_permissions(request_university_id, user_university_id):
        university_user = RequestsPermissions.get_university_user_object(user_university_id)

        return int(request_university_id) == int(university_user.university.id)

    def get_university_user_object(user_university_id):
        return models.UniversityUser.objects.get(id = user_university_id)

class PermissionsException:
    def user_has_not_permission_exception():
        raise exceptions.AuthenticationFailed('This User does not have permission.')