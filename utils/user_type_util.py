from users import models

class UserType:
    def get_user_type(user_type):
        if user_type in models.CustomUser.user_types:
            return user_type

        raise Exception(f'User type ({user_type}) does not exist')

    def get_user_type_by_model(user_model):
        if user_model == models.UniversityUser:
            return models.CustomUser.university_user_type

        raise Exception(f'Not exist User type by this Model User ({user_model})')