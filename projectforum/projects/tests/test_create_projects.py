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
                                          first_name='Job',
                                          last_name='Carter',
                                          password='topsecret')
    user1 = user_model.objects.create_user(username='Henry',
                                           email='Henry@mail.com',
                                           first_name='Henry',
                                           last_name='Jacobs',
                                           password='topsecrets')
    user2 = user_model.objects.create_user(username='Bobicus',
                                           email='bobicus@mail.com',
                                           first_name='Bobicus',
                                           last_name='Rocketus',
                                           password='topsecretz')

    tag1 = ProjectTag.objects.create(text="iOS")
    tag2 = ProjectTag.objects.create(text="Android")
    tag3 = ProjectTag.objects.create(text="Web")

    proj = Project.objects.create(
        title="Barrel",
        description="I am the first Project alpha",
        owner=user1,
        payment=2,
        amount=10,
        status=1,
    )
    proj.tags = [tag1.pk, tag2.pk]
    proj = Project.objects.create(
        title="Azrael",
        description="I am the second Project beta",
        owner=user,
        payment=1,
        amount=1,
        status=1,
    )
    proj.tags = [tag3.pk, tag2.pk]
    proj = Project.objects.create(
        title="Cricket",
        description="I am the third Project alpha beta",
        owner=user2,
        payment=2,
        amount=1000,
        status=1,
    )
    proj.tags = [tag1.pk]
    proj = Project.objects.create(
        title="decoy",
        description="I am the fourth Project beta man",
        owner=user1,
        payment=1,
        amount=1000000,
        status=1,
    )
    proj.tags = [tag3.pk]
    proj = Project.objects.create(
        title="family guy",
        description="I am the fifth Project omega",
        owner=user,
        payment=1,
        amount=999,
        status=1,
    )
    proj.tags = [tag2.pk, tag3.pk]
    proj = Project.objects.create(
        title="fallen",
        description="I am the sixth Project alpha omega",
        owner=user2,
        payment=2,
        amount=120,
        status=1,
    )
    proj.tags = [tag2.pk]
    proj = Project.objects.create(
        title="A2",
        description="I am the seventh Project beta omega",
        owner=user,
        payment=1,
        amount=999,
        status=2,
    )
    proj.tags = [tag2.pk, tag1.pk]
    proj = Project.objects.create(
        title="A3",
        description="I am the eighth Project man beta alpha",
        owner=user2,
        payment=2,
        amount=120,
        status=3,
    )
    proj.tags = [tag3.pk, tag1.pk, tag3.pk]
    proj = Project.objects.create(
        title="A4",
        description="I am the ninth Project alpha beta omega",
        owner=user2,
        payment=2,
        amount=120,
        status=4,
    )
    proj.tags = [tag3.pk, tag1.pk]
