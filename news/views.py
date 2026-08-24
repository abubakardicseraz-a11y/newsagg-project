import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.core.management import call_command
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Article, ReadingHistory


def home(request):
    articles = Article.objects.all().order_by('-fetched_at')[:30]
    recommended = []

    if request.user.is_authenticated:
        recommended = get_recommendations(request.user)

    return render(request, 'news/home.html', {
        'articles': articles,
        'recommended': recommended,
    })


@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    ReadingHistory.objects.get_or_create(user=request.user, article=article)
    return render(request, 'news/article_detail.html', {'article': article})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def reading_history(request):
    history = ReadingHistory.objects.filter(user=request.user).select_related('article').order_by('-read_at')
    return render(request, 'news/history.html', {'history': history})


@login_required
def clear_history(request):
    if request.method == 'POST':
        ReadingHistory.objects.filter(user=request.user).delete()
    return redirect('reading_history')


def refresh_articles(request, secret):
    expected_secret = os.environ.get('REFRESH_SECRET')

    if not expected_secret or secret != expected_secret:
        return HttpResponse("Forbidden", status=403)

    call_command('fetch_news')
    return HttpResponse("Articles refreshed successfully.")


def get_recommendations(user, top_n=5):
    all_articles = list(Article.objects.all())

    if len(all_articles) < 2:
        return []

    read_ids = set(
        ReadingHistory.objects.filter(user=user).values_list('article_id', flat=True)
    )

    if not read_ids:
        return []

    texts = [f"{a.title} {a.summary}" for a in all_articles]

    vectorizer = TfidfVectorizer(stop_words='english')