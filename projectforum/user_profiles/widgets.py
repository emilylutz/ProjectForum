from django.forms.widgets import SelectMultiple
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class TagsWidget(SelectMultiple):
    """
    A SelectMultiple for tags. It doesn't render a value for the options.
    """

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            return ''  # only render selected options
        return format_html('<option{}>{}</option>',
                           selected_html,
                           force_text(option_label))
