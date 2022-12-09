from users import models

class UserType:
    super_user = 'super_user'
    university_user = 'university_user'

    user_types = [
        super_user,
        university_user
    ]

    def get_user_type(user_type):
        if user_type in UserType.user_types:
            return user_type

        raise Exception(f'User type ({user_type}) does not exist')

    def get_user_type_by_model(user_model):
        if user_model == models.UniversityUser:
            return UserType.university_user

        raise Exception(f'Model User ({user_model}) does not exist')