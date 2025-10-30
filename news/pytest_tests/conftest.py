import pytest

from django.test.client import Client

from news.models import News, Comment


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def comment(news, comment_author):
    comment = Comment.objects.create(
        news=news,
        author=comment_author,
        text='Текст комментария')
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
