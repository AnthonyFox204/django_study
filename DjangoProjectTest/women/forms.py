from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Women, Category, Husband


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел.'

    def __call__(self, value, *args, **kwargs):
        if not set(value) <= set(self.ALLOWED_CHARS):
            raise forms.ValidationError(self.message, code=self.code)


class AddPostFormOutdated(forms.Form):
    title = forms.CharField(
        min_length=5,
        max_length=255,
        label='Заголовок',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        error_messages={
            'min_length': 'Слишком короткий заголовок',
            'required': 'Без заголовка никак',
            }
        )

    slug = forms.SlugField(
        max_length=255,
        label='URL',
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов'),
            MaxLengthValidator(100, message='Максимум 100 символов'),
        ]
        )

    content = forms.CharField(
        required=False,
        label='Контент',
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        )

    is_published = forms.BooleanField(
        required=False,
        initial=True,
        label='Статус'
        )

    cat = forms.ModelChoiceField(
        label='Категории',
        empty_label='Категория не выбрана',
        queryset=Category.objects.all(),
        )

    husband = forms.ModelChoiceField(
        required=False,
        label='Муж',
        empty_label='Не замужем',
        queryset=Husband.objects.all()
        )

    def clean_title(self):
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
        title = self.cleaned_data['title']
        if not set(title) <= set(ALLOWED_CHARS):
            raise forms.ValidationError('Должны присутствовать только русские символы, дефис и пробел.')
        return title


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        label = 'Категория',
        empty_label='Категория не выбрана',
        queryset=Category.objects.all()
        )

    husband = forms.ModelChoiceField(
        required=False,
        label = 'Муж',
        empty_label='Не замужем',
        queryset=Husband.objects.all()
        )

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'title': 'Заголовок',
            'slug': 'URL',
            'content': 'Контент',
            'photo': 'Фото',
            'is_published': 'Статус',
            'tags': 'Теги',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 50:
            raise forms.ValidationError('Длина превышает 50 символов.')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='E-mail')
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
