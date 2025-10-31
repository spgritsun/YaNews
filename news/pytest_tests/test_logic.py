import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_anonym_user_cant_create_comment(client, detail_news_url, form_data):
    client.post(detail_news_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(reader_client, detail_news_url, form_data,
                                 reader, news, comment_text):
    response = reader_client.post(detail_news_url, data=form_data)
    assertRedirects(response, f'{detail_news_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == comment_text
    assert comment.news == news
    assert comment.author == reader


def test_user_cant_use_bad_words(reader_client, detail_news_url, ):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = reader_client.post(detail_news_url, data=bad_words_data)
    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0
