from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    in_menu = models.BooleanField(default=True)
    order = models.IntegerField(default=1)


class Author(models.Model):
    name = models.TextField(max_length=255)
    bio = models.TextField(max_length=255)
    avatar = models.ImageField()


class Article(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    content = models.TextField()
    short_description = models.TextField()
    main_image = models.ImageField()
    pub_date = models.DateField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    """ author связан со статьёй, если удалить автора, то и статья удляется.
        То есть при такой связи тот, у которого указывается, он зависит от того, на которого ссылается. 
    """


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    comment = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Newsletter(models.Model):
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    subscribe_date = models.DateTimeField(auto_now_add=True)
    unsubscribe_date = models.DateTimeField(null=True, blank=True)
    """
    null=True, blank=True - чтобы пустое было изначально
    """


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    articles = models.ManyToManyField(Article)