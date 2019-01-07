from django.db import models


class Sentence(models.Model):
    text = models.TextField()
    article = models.ForeignKey('Article', on_delete=models.SET_NULL, null=True, related_name='sentences')
    xml = models.TextField(blank=True, null=True)
    dtree = models.TextField(blank=True, null=True)
    ptree = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.article.title, self.text)


class Category(models.Model):
    name = models.CharField(max_length=30, null=False)
    image = models.ImageField(max_length=200, blank=True, null=True)   

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=300, null=False)
    author = models.CharField(max_length=200)
    created_date = models.DateField(blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)
    image = models.ImageField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # YouTube Link

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



