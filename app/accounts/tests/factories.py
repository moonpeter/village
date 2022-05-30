import factory
from factory.fuzzy import FuzzyChoice

from django.contrib.auth import get_user_model


class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("safe_email")
    nickname = factory.Sequence(
        lambda n: factory.Faker("first_name_female", locale="ko_KR")
    )
    username = factory.Sequence(
        lambda n: factory.Faker("first_name_female", locale="ko_KR")
    )
    mbti_type = FuzzyChoice(["INFP", "ENTP", "ENTJ", "INFJ"])
    mbti_index_0 = FuzzyChoice(["I", "E"])
    mbti_index_1 = FuzzyChoice(["N", "S"])
    mbti_index_2 = FuzzyChoice(["F", "T"])
    mbti_index_3 = FuzzyChoice(["P", "J"])
