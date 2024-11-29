# views/extras_feats.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.utils import timezone

# Create your views here.

@login_required
def drawingGenerator(request):
    context = {
        'date': timezone.now().strftime(_("%a %d %B %Y")),
        }
    return render(request, 'base/drawing_generator.html', context)
    

@login_required
def websiteReviewGenerator(request):
    context = {
        'date': timezone.now().strftime(_("%a %d %B %Y")),
        }
    return render(request, 'base/website_review_generator.html', context)
    

@login_required
def likedReviews(request):
    context = {
        'date': timezone.now().strftime(_("%a %d %B %Y")),
        }
    return render(request, 'base/liked_reviews.html', context)
    

@login_required
def extrasFeatures(request):
    context = {
        'date': timezone.now().strftime(_("%a %d %B %Y")),
        }
    return render(request, 'base/extras_features.html', context)
