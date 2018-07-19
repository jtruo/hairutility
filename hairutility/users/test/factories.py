import factory
from ..models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    id = factory.Faker('uuid4')
    password = factory.Faker('password', length=10, special_chars=True, digits=True,
                             upper_case=True, lower_case=True)
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_stylist = True
