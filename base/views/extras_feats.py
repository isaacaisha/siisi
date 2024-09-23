# views/extras_feats.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

@login_required
def drawingGenerator(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/drawing_generator.html', context)
    

@login_required
def websiteReviewGenerator(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/website_review_generator.html', context)
    

@login_required
def likedReviews(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/liked_reviews.html', context)
    

@login_required
def extrasFeatures(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/extras_features.html', context)
