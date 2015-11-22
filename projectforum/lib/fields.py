from django.core.exceptions import ValidationError
from django.forms.models import ModelMultipleChoiceField

from projectforum.lib.widgets import NoValueSelectMultipleWidget


class TagsField(ModelMultipleChoiceField):
    """
    A ModelMultipleChoiceField for tags. It makes a new instance of the tag if
    it doesn't exist.
    """
    widget = NoValueSelectMultipleWidget
    default_error_messages = {
        'invalid_tag_size': ('Invalid tag. Tags may be at most %(length)d'
                             ' characters long.')
    }

    def __init__(self, tagClass, tagField, max_length=100, required=True,
                 widget=None, label=None, initial=None, help_text='', *args,
                 **kwargs):
        self.tagClass = tagClass
        self.tagField = tagField
        self.max_length = max_length
        qs = tagClass.objects.all()
        super(TagsField, self).__init__(qs, required, widget, label, initial,
                                        help_text, *args, **kwargs)

    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'],
                                  code='required')
        elif not self.required and not value:
            return self.queryset.none()
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['list'], code='list')
        for val in value:
            if len(val) > self.max_length:
                raise ValidationError(self.error_messages['invalid_tag_size'],
                                      code='invalid_tag_size',
                                      params={'length': self.max_length})
        value = self._create_values_if_needed(value)
        return super(TagsField, self).clean(value)

    def _create_values_if_needed(self, value):
        """
        Given a list of possible PK values, creates any tags that don't exist
        and replace it with the PK value.
        """
        # deduplicate given values to avoid creating many querysets or
        # requiring the database backend deduplicate efficiently.
        try:
            value = frozenset(value)
        except TypeError:
            # list of lists isn't hashable, for example
            raise ValidationError(
                self.error_messages['list'],
                code='list',
            )
        finalValue = list()
        for val in value:
            try:
                existingTag = self.queryset.filter(**{self.tagField: val})
                if existingTag:
                    finalValue.append(existingTag[0].pk)
                else:
                    tag = self.tagClass(**{self.tagField: val})
                    tag.save()
                    finalValue.append(tag.pk)
            except (ValueError, TypeError):
                tag = self.tagClass(**{self.tagField: val})
                tag.save()
                finalValue.append(tag.pk)
        return finalValue
