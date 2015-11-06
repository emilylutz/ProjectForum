from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.test import TestCase
from django.test.utils import override_settings

import mock

from .backend import MailgunAPIError, MailgunBackend


def simple_post(url, auth, data, headers):
    class MockResponse:
        pass
    response = MockResponse()
    response.status_code = 200
    return response


def fail_post(url, auth, data, headers):
    class MockResponse:
        pass
    response = MockResponse()
    response.status_code = 500
    return response


class MailgunTest(TestCase):

    @override_settings()
    def test_send_no_mailgun_settings(self):
        del settings.MAILGUN_ACCESS_KEY
        del settings.MAILGUN_SERVER_NAME
        with self.assertRaises(AttributeError):
            backend = MailgunBackend()

    @override_settings()
    def test_send_no_mailgun_settings_fail_silently(self):
        del settings.MAILGUN_ACCESS_KEY
        del settings.MAILGUN_SERVER_NAME
        backend = MailgunBackend(fail_silently=True)

    @override_settings(MAILGUN_ACCESS_KEY='key', MAILGUN_SERVER_NAME='server')
    @mock.patch('requests.post', side_effect=simple_post)
    def test_send_no_emails(self, requests_post):
        backend = MailgunBackend()
        backend.open()
        count = backend.send_messages([])
        self.assertEqual(count, None)
        backend.close()
        requests_post.assert_not_called()

    @override_settings(MAILGUN_ACCESS_KEY='key', MAILGUN_SERVER_NAME='server')
    @mock.patch('requests.post', side_effect=simple_post)
    def test_send_no_recipients(self, requests_post):
        backend = MailgunBackend()
        backend.open()
        email_message = EmailMultiAlternatives('subject', 'body', 'from_email',
                                               [])
        email_message.attach_alternative('html_body', 'text/html')
        count = backend.send_messages([email_message])
        backend.close()
        self.assertEqual(count, 0)

    @override_settings(MAILGUN_ACCESS_KEY='key', MAILGUN_SERVER_NAME='server')
    @mock.patch('requests.post', side_effect=simple_post)
    def test_send_email(self, requests_post):
        backend = MailgunBackend()
        backend.open()
        email_message = EmailMultiAlternatives('subject', 'body', 'from_email',
                                               ['to_email'])
        email_message.attach_alternative('html_body', 'text/html')
        count = backend.send_messages([email_message])
        backend.close()

        self.assertEqual(count, 1)
        self.assertEqual(requests_post.call_args, mock.call(
            u'https://api.mailgun.net/v3/server/messages',
            auth=(u'api', 'key'),
            data=[(u'to', u'to_email'), (u'text', 'body'),
                  (u'subject', 'subject'), (u'from', u'from_email'),
                  (u'html', 'html_body')],
            headers=None))

    @override_settings(MAILGUN_ACCESS_KEY='key', MAILGUN_SERVER_NAME='server')
    @mock.patch('requests.post', side_effect=fail_post)
    def test_send_email_and_fail_silently(self, requests_post):
        backend = MailgunBackend(fail_silently=True)
        backend.open()
        email_message = EmailMultiAlternatives('subject', 'body', 'from_email',
                                               ['to_email'])
        email_message.attach_alternative('html_body', 'text/html')
        count = backend.send_messages([email_message])
        backend.close()

        self.assertEqual(count, 0)
        self.assertEqual(requests_post.call_args, mock.call(
            u'https://api.mailgun.net/v3/server/messages',
            auth=(u'api', 'key'),
            data=[(u'to', u'to_email'), (u'text', 'body'),
                  (u'subject', 'subject'), (u'from', u'from_email'),
                  (u'html', 'html_body')],
            headers=None))

    @override_settings(MAILGUN_ACCESS_KEY='key', MAILGUN_SERVER_NAME='server')
    @mock.patch('requests.post', side_effect=fail_post)
    def test_send_email_and_fail(self, requests_post):
        backend = MailgunBackend()
        backend.open()
        email_message = EmailMultiAlternatives('subject', 'body', 'from_email',
                                               ['to_email'])
        email_message.attach_alternative('html_body', 'text/html')
        with self.assertRaises(MailgunAPIError):
            backend.send_messages([email_message])
        backend.close()

    @override_settings(MAILGUN_ACCESS_KEY='key', MAILGUN_SERVER_NAME='server')
    @mock.patch('requests.post', side_effect=simple_post)
    def test_send_recipient_variables(self, requests_post):
        backend = MailgunBackend()
        backend.open()
        email_message = EmailMultiAlternatives('subject', 'body', 'from_email',
                                               ['to_email'], headers={
                                               'recipient_variables':'test'})
        email_message.attach_alternative('html_body', 'text/html')
        count = backend.send_messages([email_message])
        backend.close()

        self.assertEqual(count, 1)
        self.assertEqual(requests_post.call_args, mock.call(
            u'https://api.mailgun.net/v3/server/messages',
            auth=(u'api', 'key'),
            data=[(u'to', u'to_email'), (u'text', 'body'),
                  (u'subject', 'subject'), (u'from', u'from_email'),
                  (u'recipient-variables', 'test'), (u'html', 'html_body')],
            headers=None))

    @override_settings(MAILGUN_ACCESS_KEY='key', MAILGUN_SERVER_NAME='server')
    @mock.patch('requests.post', side_effect=simple_post)
    def test_send_reply_to(self, requests_post):
        backend = MailgunBackend()
        backend.open()
        email_message = EmailMultiAlternatives('subject', 'body', 'from_email',
                                               ['to_email'],
                                               reply_to=['reply_to'])
        email_message.attach_alternative('html_body', 'text/html')
        count = backend.send_messages([email_message])
        backend.close()

        self.assertEqual(count, 1)
        self.assertEqual(requests_post.call_args, mock.call(
            u'https://api.mailgun.net/v3/server/messages',
            auth=(u'api', 'key'),
            data=[(u'to', u'to_email'), (u'text', 'body'),
                  (u'subject', 'subject'), (u'from', u'from_email'),
                  (u'html', 'html_body'), (u'h:Reply-To', u'reply_to')],
            headers=None))

    @override_settings(MAILGUN_ACCESS_KEY='key', MAILGUN_SERVER_NAME='server')
    @mock.patch('requests.post', side_effect=simple_post)
    def test_send_attachment(self, requests_post):
        backend = MailgunBackend()
        backend.open()
        email_message = EmailMultiAlternatives('subject', 'body', 'from_email',
                                               ['to_email'])
        email_message.attach_alternative('html_body', 'text/html')
        email_message.attach('test.txt', '<test></test>', 'text/html')
        count = backend.send_messages([email_message])
        backend.close()

        self.assertEqual(count, 1)
