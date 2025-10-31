from http import HTTPStatus

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


@pytest.mark.django_db
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


def test_author_can_delete_comment(comment_author_client,
                                   comment_delete_url, url_to_comments):
    response = comment_author_client.delete(comment_delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(reader_client,
                                                  comment_delete_url):
    response = reader_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        comment_author_client, comment_edit_url, comment,
        form_data_with_new_comment_text, url_to_comments, new_comment_text):
    response = comment_author_client.post(
        comment_edit_url, data=form_data_with_new_comment_text)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == new_comment_text


def test_user_cant_edit_comment_of_another_user(
        reader_client, comment_edit_url, form_data_with_new_comment_text,
        comment, comment_text):
    response = reader_client.post(comment_edit_url,
                                  data=form_data_with_new_comment_text)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
