import pytest

from django.conf import settings
from pytest_lazy_fixtures import lf

pytestmark = pytest.mark.django_db


def test_news_count(all_news, client, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(all_news, client, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(detail_news_url, client, all_comments):
    response = client.get(detail_news_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize('user_client, result', (
        (lf('reader_client'), True),
        (lf('client'), False),
))
def test_user_has_comment_form(user_client, detail_news_url, result):
    response = user_client.get(detail_news_url)
    assert ('form' in response.context) is result
