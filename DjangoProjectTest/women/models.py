from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import get_user_model


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = (0, 'Черновик')
        PUBLISHED = (1, 'Опубликовано')

    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug',
                            validators=[MinLengthValidator(5, message='Минимум 5 символов'),
                                        MaxLengthValidator(100, message='Максимум 100 символов'),])
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default=None, blank=True, null=True,
                              verbose_name='Photo')
    content = models.TextField(blank=True, verbose_name='Contents')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Updated')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Status')
    cat = models.ForeignKey(to='Category', on_delete=models.PROTECT, related_name='posts',
                            verbose_name='Category')
    tags = models.ManyToManyField(to='TagPost', blank=True, related_name='tags', verbose_name='Tags')
    husband = models.OneToOneField(to='Husband', on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name='wuman', verbose_name='Husband')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, related_name='posts',
                               verbose_name='Author', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Famous Women'
        verbose_name_plural = 'Famous Women'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Category')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
