from django.contrib.auth import get_user_model

from projectforum.projects.models import Project, ProjectTag


def create_many_projects():
    """
    Build a bunch of mock projects in case we're testing with a situation
    that needs to look at many different projects.
    """
    user_model = get_user_model()
    user = user_model.objects.create_user(username='Job',
                                          email='Job@mail.com',
                                          password='topsecret')
    user1 = user_model.objects.create_user(username='Henry',
                                           email='Henry@mail.com',
                                           password='topsecrets')
    user2 = user_model.objects.create_user(username='Bobicus',
                                           email='bobicus@mail.com',
                                           password='topsecretz')

    tag0 = ProjectTag.objects.create(text="tag0")
    tag1 = ProjectTag.objects.create(text="tag1")
    tag2 = ProjectTag.objects.create(text="tag2")

    proj = Project.objects.create(
        title="B",
        description="I am the first Project",
        owner=user1,
        payment=2,
        amount=10,
        status=1,
    )
    proj.tags=[tag0.pk, tag1.pk]
    Project.objects.create(
        title="A",
        description="I am the second Project",
        owner=user,
        payment=1,
        amount=1,
        status=1,
    )
    Project.objects.create(
        title="C",
        description="I am the third Project",
        owner=user2,
        payment=2,
        amount=1000,
        status=1,
    )
    Project.objects.create(
        title="D",
        description="I am the fourth Project",
        owner=user1,
        payment=1,
        amount=1000000,
        status=1,
    )
    Project.objects.create(
        title="F",
        description="I am the fifth Project",
        owner=user,
        payment=1,
        amount=999,
        status=1,
    )
    Project.objects.create(
        title="E",
        description="I am the sixth Project",
        owner=user2,
        payment=2,
        amount=120,
        status=1,
    )
    Project.objects.create(
        title="A2",
        description="I am the seventh Project",
        owner=user,
        payment=1,
        amount=999,
        status=2,
    )
    Project.objects.create(
        title="A3",
        description="I am the eighth Project",
        owner=user2,
        payment=2,
        amount=120,
        status=3,
    )
    Project.objects.create(
        title="A4",
        description="I am the ninth Project",
        owner=user2,
        payment=2,
        amount=120,
        status=4,
    )
