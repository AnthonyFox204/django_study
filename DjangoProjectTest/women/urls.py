from django.urls import path

from . import views
from .views import WomenHome, AddPage, WomenCategory, TagPostList, ShowPost, UpdatePage, ContactFormView


urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', UpdatePage.as_view(), name='edit_page'),
]
