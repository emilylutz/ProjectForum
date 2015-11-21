from django.http import HttpResponse

import json

from projectforum.projects.models import Project


def get_projects_by_filter(status, keywords):
    return projects_JSON_response(filter_projects(status, keywords))


def filter_projects(status, keywords):
    project_list = Project.objects.all().filter(status=status)
    for keyword in keywords:
        titles = project_list.filter(title__icontains=keyword)
        descriptions = project_list.filter(description__icontains=keyword)
        owner_first = project_list.filter(owner__first_name__icontains=keyword)
        owner_last = project_list.filter(owner__last_name__icontains=keyword)
        owner = owner_first | owner_last
        tags = project_list.filter(tags__text__icontains=keyword)
        project_list = (titles | descriptions | owner | tags).distinct()
    return project_list


def get_project_list(status, keywords, order, salary, ascending):
    try:
        project_list = filter_projects(status, keywords)
    except:
        return errorMessage(error='We were unable to filter projects')
    if len(project_list) == 0:
        return projects_JSON_response(project_list)

    if order == 'payment':
        try:
            projects = sort_projects_by_payment(salary=salary,
                                                ascending=ascending,
                                                project_list=project_list)
            return projects_JSON_response(projects)
        except:
            return errorMessage(error='Error when sorting by payment')
    elif order == 'timestamp':
        try:
            projects = sort_projects_by_timestamp(ascending=ascending,
                                                  project_list=project_list)
            return projects_JSON_response(projects)
        except:
            return errorMessage(error='Error when sorting by timestamp')
    elif order == 'title':
        try:
            projects = sort_projects_by_title(ascending=ascending,
                                              project_list=project_list)
            return projects_JSON_response(projects)
        except:
            return errorMessage(error='Error when sorting by title')

    return errorMessage(error='Something went wrong when handling your query')


def get_projects(status, keywords, order, salary, ascending):
    project_list = filter_projects(status, keywords)

    if len(project_list) == 0:
        return project_list

    if order == 'payment':
        projects = sort_projects_by_payment(salary=salary,
                                            ascending=ascending,
                                            project_list=project_list)
        return projects
    elif order == 'timestamp':
        projects = sort_projects_by_timestamp(ascending=ascending,
                                              project_list=project_list)
        return projects
    elif order == 'title':
        projects = sort_projects_by_title(ascending=ascending,
                                          project_list=project_list)
        return projects


def sort_projects_by_timestamp(ascending, project_list):
    order = 'timestamp'
    if not ascending:
        order = '-' + order
    list_of_projects = project_list.order_by(order)
    return list_of_projects


def sort_projects_by_title(ascending, project_list):
    order = 'title'
    if not ascending:
        order = '-' + order
    list_of_projects = project_list.order_by(order)
    return list_of_projects


def sort_projects_by_payment(salary, ascending, project_list):
    order = 'payment'
    if salary != 'hourly' and salary != 'lump':
        return errorMessage(error='Please check your salary in Get request')
    if salary == 'hourly':
        order = '-' + order
    amount = 'amount'
    if not ascending:
        amount = '-' + amount
    list_of_projects = project_list.order_by(order, amount)
    return list_of_projects


def projects_JSON_response(projects):
    projects_json = {
        "status": 1,
        "projects": []
    }
    # Go through each individual project and JSONify it.
    for the_project in projects:
        tags = list()
        for tag in the_project.tags.all():
            tags.append(tag.text)
        projects_json['projects'].append({
            'id': the_project.id,
            'title': the_project.title,
            'description': the_project.description,
            'owner': the_project.owner.username,
            'payment': the_project.payment,
            'amount': the_project.amount,
            'status': the_project.status,
            'tags': tags,
            'timestamp': format_time(the_project.timestamp)
        })
    return HttpResponse(json.dumps(projects_json),
                        content_type='application/json')


def format_time(database_time):
    return database_time.strftime("%b %d %Y at %I:%M")


def convert_people_to_list(peoples):
    """
    Pass in a list of people (User Model)
    It will then translate it into list form, showing only the username
    """
    people_JSON = []
    for person in peoples:
        people_JSON.append(person.username)
    return people_JSON


def errorMessage(error="Apologies, we couldn't process your request."):
    response = {
        "status": -1,
        "errors": str(error)
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


# def check_length(start, end, projects):
#     """
#     Make sure the length is within confines.  Will throw an error if I can't
#     get any projects based on the limits, otherwise will make sure I don't
#     overflow.
#     """
#     length_projects = len(projects)
#     if length_projects < start:
#         return -1
#     if length_projects > end:
#         return end
#     return length_projects
