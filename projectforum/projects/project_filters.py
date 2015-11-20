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


def get_project_list(status, keywords, order, salary, ascending,
                     starting_from, ending_at):
    # Sorting is a little more complicated in the case of sort by payment
    try:
        project_list = filter_projects(status, keywords)
        if len(project_list) == 0:
            return projects_JSON_response(project_list)
        if order == 'payment':
            if salary == 'Hourly':
                order = '-' + order
            amount = 'amount'
            if not ascending:
                amount = '-' + amount
            list_of_projects = project_list.order_by(order, amount)
            quant_proj = check_length(starting_from, ending_at,
                                      list_of_projects
                                      )
            if quant_proj == -1:
                return errorMessage(error="We cannot provide starting from"
                                          "minimum limit of projects")
            return projects_JSON_response(list_of_projects[
                                              starting_from-1:quant_proj
                                          ])
        # For every other type of sorting
        if not ascending:
            # If I'm sorting by descending, add negative to get descending
            order = '-' + order
        list_of_projects = project_list.order_by(order)
        quant_proj = check_length(starting_from, ending_at, list_of_projects)
        if quant_proj == -1:
            return errorMessage(error="We cannot provide starting from"
                                      " minimum limit of projects")
        return projects_JSON_response(list_of_projects[
                                          starting_from-1: quant_proj
                                      ])
    except:
        return errorMessage()


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
            'timestamp': format_time(the_project.timestamp),
            'team_members': convert_people_to_list(
                                the_project.team_members.all()
                            ),
            'applicants': convert_people_to_list(the_project.applicants.all())
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


def errorMessage(error="Apologies, we could not process the request you've"
                       " made."):
    response = {
        "status": -1,
        "errors": str(error)
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


def check_length(start, end, projects):
    """
    Make sure the length is within confines.  Will throw an error if I can't
    get any projects based on the limits, otherwise will make sure I don't
    overflow.
    """
    length_projects = len(projects)
    if length_projects < start:
        return -1
    if length_projects > end:
        return end
    return length_projects
