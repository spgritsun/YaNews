from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf

from django.urls import reverse


@pytest.mark.parametrize('name, flag, status', (
        ('news:home', None, HTTPStatus.OK),
        ('news:detail', True, HTTPStatus.OK),
        ('users:login', None, HTTPStatus.OK),
        ('users:signup', None, HTTPStatus.OK),
        ('users:logout', None, HTTPStatus.METHOD_NOT_ALLOWED),
))
def test_pages_availability(name, news, flag, client, status):
    args = (news.id,) if flag else None
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == status


def test_logout_for_post_method(client):
    name = 'users:logout'
    url = reverse(name)
    response = client.post(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('user_client, status', (
        (lf('comment_author_client'), HTTPStatus.OK),
        (lf('reader_client'), HTTPStatus.NOT_FOUND),
))
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_availability_for_comment_edit_and_delete(
        status, name, comment, user_client):
    url = reverse(name, args=(comment.id,))
    response = user_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_redirect_for_anonymous_client(name, comment, client):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
