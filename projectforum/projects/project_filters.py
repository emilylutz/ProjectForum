import json

from .models import Project
from django.http import HttpResponse

# Ignore salary_type for now
def get_project_list(order, salary, ascending, starting_from, ending_at):
    # Sorting is a little more complicated in the case of sort by payment
    if order == 'payment':
        if salary == 'Lump Sum':
            order = '-' + order
        amount = 'amount'
        if not ascending:
            amount = '-' + amount
        try:
            return projects_JSON_response(Project.objects.all().order_by(order).order_by(amount))
        except:
            return errorMessage()

    # For every other type of sorting
    if not ascending:
        # If I'm sorting by descending, add the negative to the query to denote it
        order = '-' + order
    # try:
    return projects_JSON_response(list(Project.objects.all().order_by('timestamp')))
    # except:
        # return errorMessage(error=Project.objects.all())


def projects_JSON_response(projects):
    projects_json = {
        "status": 1,
        "projects": []
    }

    for the_project in projects_json:
        projects_json['projects'].append({
            'title': the_project.title,
            'description': the_project.description,
            'owner': the_project.owner,
            'payment': the_project.payment,
            'amount': the_project.amount,
            'status': the_project.status,
            'tags': the_project.tags,
            'timestamp': the_project.timestamp,
            'team_members': the_project.team_members,
            'applicants': the_project.applicants
        })
    return HttpResponse(json.dumps(projects_json),
                        content_type='application/json')

def errorMessage(error="Apologies, we could not process the request you've made."):
    response = {
        "status": -1,
        "errors": str(error)
    }
    return HttpResponse(json.dumps(response), content_type='application/json')
