from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf

from django.urls import reverse


@pytest.mark.parametrize('name, args', (
        ('news:home', None),
        ('news:detail', lf('news_id_for_args')),
        ('users:login', None),
        ('users:signup', None),
))
@pytest.mark.django_db
def test_pages_availability(name, args, client):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('user_client, status', (
        (lf('comment_author_client'), HTTPStatus.OK),
        (lf('reader_client'), HTTPStatus.NOT_FOUND),
))
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
@pytest.mark.django_db
def test_availability_for_comment_edit_and_delete(
        status, name, comment_id_for_args, user_client):
    url = reverse(name, args=comment_id_for_args)
    response = user_client.get(url)
    assert response.status_code == status
