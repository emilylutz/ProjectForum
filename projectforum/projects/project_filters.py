import json

from .models import Project
from django.http import HttpResponse

# Ignore salary_type for now
def get_project_list(status, order, salary, ascending, starting_from, ending_at):
    # Sorting is a little more complicated in the case of sort by payment
    # try:
    project_list = Project.objects.all().filter(status=status)
    if order == 'payment':
        if salary == 'Lump':
            salary = 'Lump Sum'
        if salary == 'Hourly':
            order = '-' + order
        amount = 'amount'
        if not ascending:
            amount = '-' + amount
            return projects_JSON_response(project_list.order_by(order, amount))
    # For every other type of sorting
    if not ascending:
        # If I'm sorting by descending, add the negative to the query to denote it
        order = '-' + order
    return projects_JSON_response(project_list.order_by(order))
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
