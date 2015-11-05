from django.shortcuts import render
from .forms import *

# Create your views here.

def make_review(request):
    if request.method == 'POST':
        rating_form = RatingForm(data=request.POST)
        rating = rating_form.save(commit=False)
        rating.user = request.user
        rating.save()
    else:
        rating_form = RatingForm()
    return render(request, 'reviews.html', {'form': rating_form})
