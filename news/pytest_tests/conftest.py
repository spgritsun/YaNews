from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import News, Comment


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def comment_text():
    comment_text = 'Текст комментария'
    return comment_text


@pytest.fixture
def new_comment_text():
    new_comment_text = 'Обновлённый комментарий'
    return new_comment_text


@pytest.fixture
def comment(news, comment_author, comment_text):
    comment = Comment.objects.create(
        news=news,
        author=comment_author,
        text=comment_text)
    return comment


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def comment_author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def comment_author_client(comment_author):
    client = Client()
    client.force_login(comment_author)
    return client


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def news_id_for_args(news):
    return (news.id,)


@pytest.fixture
def comment_id_for_args(comment):
    return (comment.id,)


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def home_url():
    home_url = reverse('news:home')
    return home_url


@pytest.fixture
def detail_news_url(news_id_for_args):
    detail_news_url = reverse('news:detail', args=news_id_for_args)
    return detail_news_url


@pytest.fixture
def now():
    now = timezone.now()
    return now


@pytest.fixture
def all_comments(news, comment_author, now):
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=comment_author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data(comment_text):
    form_data = {'text': comment_text}
    return form_data


@pytest.fixture
def form_data_with_new_comment_text(new_comment_text):
    new_form_data = {'text': new_comment_text}
    return new_form_data


@pytest.fixture
def url_to_comments(detail_news_url):
    url_to_comments = detail_news_url + '#comments'
    return url_to_comments


@pytest.fixture
def comment_edit_url(comment_id_for_args):
    comment_edit_url = reverse('news:edit', args=comment_id_for_args)
    return comment_edit_url


@pytest.fixture
def comment_delete_url(comment_id_for_args):
    comment_delete_url = reverse('news:delete', args=comment_id_for_args)
    return comment_delete_url
