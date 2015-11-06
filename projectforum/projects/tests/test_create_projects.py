from .models import Project
from django.contrib.auth.models import User

"""
Build a bunch of mock projects in case we're testing with a situation
that needs to look at many different projects.
"""
def create_many_projects():
    user = User.objects.create_user(username='Job',
                                     email='Job@gmail.com',
                                     password='topsecret')
    user1 = User.objects.create_user(username='Henry',
                                         email='Henry@gmail.com',
                                         password='topsecrets')
    user2 = User.objects.create_user(username='Bobicus',
                                         email='bobicus@gmail.com',
                                         password='topsecretz')
    Project.objects.create(
        title = "B",
        description = "I am the first Project",
        owner = user1,
        payment = 2,
        amount = 10,
        status = 1,
    )
    Project.objects.create(
        title = "A",
        description = "I am the second Project",
        owner = user,
        payment = 1,
        amount = 1,
        status = 1,
    )
    Project.objects.create(
        title = "C",
        description = "I am the third Project",
        owner = user2,
        payment = 2,
        amount = 1000,
        status = 1,
    )
    Project.objects.create(
        title = "D",
        description = "I am the fourth Project",
        owner = user1,
        payment = 1,
        amount = 1000000,
        status = 1,
    )
    Project.objects.create(
        title = "F",
        description = "I am the fifth Project",
        owner = user,
        payment = 1,
        amount = 999,
        status = 1,
    )
    Project.objects.create(
        title = "E",
        description = "I am the sixth Project",
        owner = user2,
        payment = 2,
        amount = 120,
        status = 1,
    )
    Project.objects.create(
        title = "A2",
        description = "I am the seventh Project",
        owner = user,
        payment = 1,
        amount = 999,
        status = 2,
    )
    Project.objects.create(
        title = "A3",
        description = "I am the eighth Project",
        owner = user2,
        payment = 2,
        amount = 120,
        status = 3,
    )
    Project.objects.create(
        title = "A4",
        description = "I am the ninth Project",
        owner = user2,
        payment = 2,
        amount = 120,
        status = 4,
    )
