from django.db import models
from django.contrib.auth.models import User

SOURCE_COLORS = {
    "BBC News": "#3D7BFA",
    "TechCrunch": "#8B5CF6",
    "BBC Business": "#F59E0B",
    "ESPN": "#10B981",
}


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=300)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    url = models.URLField(unique=True)
    source = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    @property
    def badge_color(self):
        return SOURCE_COLORS.get(self.source, "#6B7280")

    def __str__(self):
        return self.title


class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} read {self.article.title}"