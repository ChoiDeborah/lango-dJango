from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db.models import TextField


class PatternType(models.Model):
    id = models.AutoField(primary_key=True)
    pattern_type = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.pattern_type


class PatternCategory(models.Model):
    id = models.AutoField(primary_key=True)
    pattern_category = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.pattern_category


class Pattern(models.Model):
    pattern_name = models.CharField(max_length=100, blank=False, null=False)
    pattern_Type_id = models.ForeignKey('PatternType', on_delete=models.CASCADE, related_name='patterntag')
    Pattern_Category_id = models.ForeignKey('PatternCategory', on_delete=models.CASCADE, related_name='categorytag')

    def __str__(self):
        return '{}({})'.format(self.pattern_Type_id, self.Pattern_Category_id)


class Sentence(models.Model):
    sentence = models.TextField(blank=False, null=False)
    article = models.ForeignKey('Article', on_delete=models.SET_NULL, related_name='sentences', null=True)
    released_date = models.DateField(blank=False, null=False)
    difficulty = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True,
                                validators=[MaxValueValidator(100), MinValueValidator(0)])
    xml = models.TextField(blank=False, null=False)
    source_link = models.CharField(max_length=200, blank=True, null=True)
    youtube_link = models.URLField(max_length=200, blank=True, null=True)
    pattern = models.ManyToManyField(Pattern, blank=True)

    # pattern 여러개 선택할 수 있게 만들기



    # dtree = models.TextField(blank=True, null=True)
    # ptree = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.article.title, self.sentence)


class Pos(models.Model):
    sentence = models.ForeignKey('Sentence', on_delete=models.CASCADE, related_name='pos')
    word = models.TextField(blank=False, null=False)
    lemma = models.TextField(blank=False, null=False)
    char_begin = models.IntegerField(blank=False, null=False)
    char_end = models.IntegerField(blank=False, null=False)
    POS = models.TextField(blank=False, null=False)
    NER = models.TextField(blank=False, null=False)

    def __str__(self):
        return 'POS({}): {}/{}({}-{})'\
            .format(self.sentence.sentence, self.POS, self.NER, self.char_begin, self.char_end)


class Dependency(models.Model):
    sentence = models.ForeignKey('Sentence', on_delete=models.CASCADE, related_name='dependency')
    dependencies = models.TextField(blank=False, null=False)
    governor = models.TextField(blank=False, null=False)
    dependent = models.TextField(blank=False, null=False)

    def __str__(self):
        return 'Dependency({}): ({}) --{}-> ({})'\
            .format(self.sentence.sentence, self.dependencies, self.governor, self.dependent)


class Category(models.Model):
    title = models.CharField(max_length=30, null=False)
    image = models.ImageField(max_length=200, blank=True, null=True)   

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=300, blank=False, null=False)
    author = models.CharField(max_length=200, blank=False, null=False)
    categories = models.ManyToManyField(Category, related_name='articles')
    created_date = models.DateField(blank=True, null=True)
    source_link = models.CharField(max_length=200, blank=True, null=True)
    youtube_link = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title






