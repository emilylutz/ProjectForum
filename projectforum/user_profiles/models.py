from datetime import tzinfo, timedelta, datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from projectforum.projects.models import Project

import hashlib
import random
import re


class UTC(tzinfo):
    """ UTC time zone information. """

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


class RegistrationLinkManager(models.Manager):
    """
    Custom manager for the ``RegistrationLink`` model.
    """

    def activate_by_key(self, activation_key):
        """
        Validate a key and activate the corresponding ``User`` if it exists.
        """
        if not re.compile('^[a-f0-9]{40}$').search(activation_key):
            return False

        try:
            link = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False

        if not link.is_activation_key_expired():
            user = link.user
            user.is_active = True
            user.save()
            link.delete()

            profile = UserProfile.objects.get_or_create_profile(user)

            return user
        return False

    def create_inactive_user(self, site, new_user, request):
        """
        Creates an inactive ``User`` with an associated ``RegistrationLink``.
        Sends an email with the link.
        """
        new_user.is_active = False
        new_user.save()

        salt = (hashlib.sha1(str(random.random()).encode('ascii'))
                       .hexdigest()[:5]).encode('ascii')
        user_pk = str(new_user.pk)
        if isinstance(user_pk, unicode):
            user_pk = user_pk.encode('utf-8')
        activation_key = hashlib.sha1(salt + user_pk).hexdigest()

        link = self.create(user=new_user, activation_key=activation_key)
        link.send_activation_email(site, request)

        return new_user

    def delete_expired_users(self):
        """
        Deletes ```RegistrationLink``s that are no longer valid.
        """
        for link in self.all():
            try:
                if link.is_activation_key_expired():
                    user = link.user
                    if not user.is_active:
                        user.delete()
                        link.delete()
            except get_user_model().DoesNotExist:
                link.delete()


class RegistrationLink(models.Model):
    """
    A link which stores an activation key for user account registration.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='user')
    activation_key = models.CharField('activation key', max_length=40)

    objects = RegistrationLinkManager()

    class Meta:
        verbose_name = 'registration link'
        verbose_name_plural = 'registration links'

    def __unicode__(self):
        return "Registration link for %s" % self.user

    def is_activation_key_expired(self):
        """
        Determine whether this ``RegistrationLink``'s activation key is
        expired.
        """
        life = timedelta(days=settings.REGISTRATION_LINK_LIFE)
        now = datetime.utcnow()
        now = now.replace(tzinfo=UTC())
        return (self.user.date_joined + life <= now)

    def send_activation_email(self, site, request=None):
        """
        Send an activation email to the user associated.
        """
        context = {}
        if request is not None:
            context = RequestContext(request, context)
        context.update({
            'user': self.user,
            'activation_key': self.activation_key,
            'expiration_days': settings.REGISTRATION_LINK_LIFE,
            'site': site,
        })

        subject = render_to_string('activation_email_subject.txt', context)
        subject = ''.join(subject.splitlines())
        body = render_to_string('activation_email.txt', context)
        html_body = render_to_string('activation_email.html', context)
        from_email = settings.REGISTRATION_FROM_ADDRESS
        to_emails = [self.user.email]

        from django.core.mail import send_mail

        email_message = EmailMultiAlternatives(subject, body, from_email,
                                               to_emails)
        email_message.attach_alternative(html_body, 'text/html')
        email_message.send()


class UserSkillTag(models.Model):
    """
    The user can be tagged with skills. Each tag is a skill.
    """
    max_length = 100
    skill = models.CharField(max_length=max_length)

    def __unicode__(self):
        return self.skill

    class Meta:
        verbose_name = 'user skill tag'
        verbose_name_plural = 'user skill tags'

    def __unicode__(self):
        return "User skill %s" % self.skill


class UserProfileManager(models.Manager):
    """
    Custom manager for the ``UserProfile`` model.
    """

    def get_or_create_profile(self, user):
        """
        Get the user's profile (creating it if necessary).
        """
        try:
            return self.get(user=user)
        except self.model.DoesNotExist:
            profile = self.create(user=user)
            return profile


class UserProfile(models.Model):
    """
    The unrequired user information for filling out the user profile.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='user')

    openToEmploy = models.BooleanField('Open to full time employment',
                                       default=False)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in " +
                                         "the format: '+999999999'. Up to " +
                                         "15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True,
                                    max_length=15)

    github = models.URLField('GitHub url', blank=True)
    linkedin = models.URLField('Linkedin url', blank=True)
    personal = models.URLField('Personal url', blank=True)

    skills = models.ManyToManyField(UserSkillTag, related_name='user_profiles',
                                    blank=True)

    showPastProjects = models.BooleanField('Publicly show past projects',
                                           default=False)

    showRatings = models.BooleanField('Public show ratings',
                                      default=False)

    bookmarked_projects = models.ManyToManyField(Project, blank=True)
    objects = UserProfileManager()

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'

    def __unicode__(self):
        return "User profile for %s" % self.user
