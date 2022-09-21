import pytest

from users.models import User

user: User = None
username = 'john doe'

def before_each():
    print('BEFORE EACH')
    User.objects.create(name='john doe')

def after_each():
    print('AFTER EACH')
    User.objects.all().delete()

# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test
@pytest.fixture(autouse=True)
def before_after_each():
    before_each()
    yield
    after_each()


@pytest.mark.django_db
def test_user_does_not_exist():
    User.objects.filter(name=username).delete()

    with pytest.raises(Exception) as e:
        User.objects.get(name=username)

    assert 'User matching query does not exist' in str(e.value)

@pytest.mark.django_db
def test_user_2():
    user = User.objects.get(name=username)
    assert user != None