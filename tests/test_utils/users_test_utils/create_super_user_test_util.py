from users.models import CustomUser

class CreateSuperUserTestUtil:
    super_user_dicts = [
        {
            "first_name": "super",
            "last_name": "admin",
            "email": "admin@admin.com",
            "password": "12345",
            "type": "super_user"
        }
    ]
    
    def create_super_user(index = None):
        if not index:
            index = 0

        Super_user_dict = CreateSuperUserTestUtil.get_super_user_dict(index)

        Super_user = CustomUser.objects.create(
            first_name = Super_user_dict['first_name'],
            last_name = Super_user_dict['last_name'],
            email = Super_user_dict['email'],
            password = Super_user_dict['password'])

        return Super_user

    def get_super_user_dict(index):
        return CreateSuperUserTestUtil.super_user_dicts[index]
