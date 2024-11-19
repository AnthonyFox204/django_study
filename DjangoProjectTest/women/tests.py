from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Women


class GetPagesTestCase(TestCase):
    fixtures = (
        'women_women.json',
        'women_category.json',
        'women_husband.json',
        'women_tagpost.json',
    )

    def setUp(self):
        '''Actions before test.'''

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        posts = Women.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerysetEqual(response.context_data['posts'], posts[:5])  # 5 because of pagination.

    def test_paginate_mainpage(self):
        page = 2
        paginate_by = 5
        path = reverse('home')
        response = self.client.get(path + f'?page={page}')
        posts = Women.published.all().select_related('cat')
        start = (page-1) * paginate_by
        end = page * paginate_by
        self.assertQuerysetEqual(response.context_data['posts'], posts[start:end])

    def test_content_post(self):
        post = Women.published.get(pk=1)
        path = reverse('post', args=(post.slug,))
        response = self.client.get(path)
        self.assertEqual(post.content, response.context_data['post'].content)

    def tearDown(self):
        '''Actions after test.'''
