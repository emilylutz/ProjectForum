import json

from .models import Project
from django.http import HttpResponse

def get_project_list(status, order, salary, ascending, starting_from, ending_at):
    # Sorting is a little more complicated in the case of sort by payment
    # try:
    project_list = Project.objects.all().filter(status=status)
    if order == 'payment':
        if salary == 'Hourly':
            order = '-' + order
        amount = 'amount'
        if not ascending:
            amount = '-' + amount
        list_of_projects = project_list.order_by(order, amount)
        quant_proj = check_length(starting_from, ending_at, list_of_projects)
        if quant_proj == -1:
            return errorMessage(error="We cannot provide starting from minimum limit of projects")
        return projects_JSON_response(list_of_projects[starting_from-1: quant_proj])
    # For every other type of sorting
    if not ascending:
        # If I'm sorting by descending, add the negative to the query to denote it
        order = '-' + order
    list_of_projects = project_list.order_by(order)
    quant_proj = check_length(starting_from, ending_at, list_of_projects)
    if quant_proj == -1:
        return errorMessage(error="We cannot provide starting from minimum limit of projects")
    return projects_JSON_response(list_of_projects[starting_from-1: quant_proj])
    # except:
    #     return errorMessage()


def projects_JSON_response(projects):
    projects_json = {
        "status": 1,
        "projects": []
    }
    # Go through each individual project and JSONify it.
    for the_project in projects:
        projects_json['projects'].append({
            'title': the_project.title,
            'description': the_project.description,
            'owner': the_project.owner.username,
            'payment': the_project.payment,
            'amount': the_project.amount,
            'status': the_project.status,
            'tags': the_project.tags,
            'timestamp': format_time(the_project.timestamp),
            'team_members': convert_people_to_list(the_project.team_members.all()),
            'applicants': convert_people_to_list(the_project.applicants.all())
        })
    return HttpResponse(json.dumps(projects_json),
                        content_type='application/json')

def format_time(database_time):
    return database_time.strftime("%b %d %Y at %I:%M")

"""
Pass in a list of people (User Model)
It will then translate it into list form, showing only the username
"""
def convert_people_to_list(peoples):
    people_JSON = []
    for person in peoples:
        people_JSON.append(person.username)
    return people_JSON

def errorMessage(error="Apologies, we could not process the request you've made."):
    response = {
        "status": -1,
        "errors": str(error)
    }
    return HttpResponse(json.dumps(response), content_type='application/json')

"""
Make sure the length is within confines.  Will throw an error if I can't get any
projects based on the limits, otherwise will make sure I don't overflow
"""
def check_length(start, end, projects):
    length_projects = len(projects)
    if length_projects < start:
        return -1
    if length_projects > end:
        return end
    return length_projects
