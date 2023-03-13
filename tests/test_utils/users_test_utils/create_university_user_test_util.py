from users.models import UniversityUser

class CreateUniversityUserTestUtil:
    university_user_dicts = [
        {
            "first_name": "Arnold",
            "last_name": "Schwarzenegger",
            "email": "arnold@user.com",
            "password": "12345",
            "type": "university_user"
        },
        {
            "first_name": "Ronnie",
            "last_name": "Coleman",
            "email": "ronnie@user.com",
            "password": "12345",
            "type": "university_user"
        },
        {
            "first_name": "Phil",
            "last_name": "Heath",
            "email": "phil@user.com",
            "password": "12345",
            "type": "university_user"
        },
    ]
    
    def create_university_user(index, university):
        university_user_dict = CreateUniversityUserTestUtil.get_university_user_dict(index)

        university_user = UniversityUser.objects.create(
            first_name = university_user_dict['first_name'],
            last_name = university_user_dict['last_name'],
            email = university_user_dict['email'],
            password = university_user_dict['password'],
            university = university)

        return university_user

    def get_university_user_dict(index):
        return CreateUniversityUserTestUtil.university_user_dicts[index]
