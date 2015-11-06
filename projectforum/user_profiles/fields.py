from django.core.exceptions import ValidationError
from django.forms.models import ModelMultipleChoiceField

from .models import UserSkillTag
from .widgets import TagsWidget


class TagsField(ModelMultipleChoiceField):
    """
    A ModelMultipleChoiceField for tags. It makes a new instance of the tag if
    it doesn't exist.
    """
    widget = TagsWidget

    def __init__(self, required=True, widget=None, label=None, initial=None,
                 help_text='', *args, **kwargs):
        qs = UserSkillTag.objects.all()
        super(TagsField, self).__init__(qs, required, widget, label, initial,
            help_text, *args, **kwargs)

    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
        elif not self.required and not value:
            return self.queryset.none()
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['list'], code='list')
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
        for skill in value:
            try:
                skillTag = self.queryset.filter(**{'skill': skill})
                if skillTag:
                    finalValue.append(skillTag[0].pk)
                else:
                    tag = UserSkillTag(skill=skill)
                    tag.save()
                    finalValue.append(tag.pk)
            except (ValueError, TypeError):
                tag = UserSkillTag(skill=skill)
                tag.save()
                finalValue.append(tag.pk)
        return finalValue
