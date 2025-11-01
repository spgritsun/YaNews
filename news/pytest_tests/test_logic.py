from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'
FORM_DATA = {'text': COMMENT_TEXT}
FORM_DATA_WITH_NEW_COMMENT = {'text': NEW_COMMENT_TEXT}


def test_anonym_user_cant_create_comment(client, detail_news_url):
    initial_comment_count = Comment.objects.count()
    client.post(detail_news_url, data=FORM_DATA)
    assert Comment.objects.count() == initial_comment_count


def test_user_can_create_comment(reader_client, detail_news_url, reader, news):
    initial_comment_count = Comment.objects.count()
    response = reader_client.post(detail_news_url, data=FORM_DATA)
    assertRedirects(response, f'{detail_news_url}#comments')
    assert Comment.objects.count() == initial_comment_count + 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == reader


@pytest.mark.parametrize('bad_words', BAD_WORDS)
def test_user_cant_use_bad_words(reader_client, detail_news_url, bad_words):
    bad_words_data = {'text': f'Какой-то текст, {bad_words}, еще текст'}
    initial_comment_count = Comment.objects.count()
    response = reader_client.post(detail_news_url, data=bad_words_data)
    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )

    assert Comment.objects.count() == initial_comment_count


def test_author_can_delete_comment(comment_author_client, comment,
                                   comment_delete_url, url_to_comments):
    initial_comment_count = Comment.objects.count()
    response = comment_author_client.delete(comment_delete_url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == initial_comment_count - 1
    assert not Comment.objects.filter(id=comment.id).exists()


def test_user_cant_delete_comment_of_another_user(reader_client, comment,
                                                  comment_delete_url):
    initial_comment_count = Comment.objects.count()
    response = reader_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_comment_count
    assert Comment.objects.filter(id=comment.id).exists()

def test_author_can_edit_comment(
        comment_author_client, comment_edit_url, comment, url_to_comments):
    response = comment_author_client.post(
        comment_edit_url, data=FORM_DATA_WITH_NEW_COMMENT)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
        reader_client, comment_edit_url, comment):
    response = reader_client.post(comment_edit_url,
                                  data=FORM_DATA_WITH_NEW_COMMENT)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
