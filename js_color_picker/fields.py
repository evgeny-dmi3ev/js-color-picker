from __future__ import unicode_literals

from django.core.checks import Error
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import CharField
from django.conf import settings

from . import forms, widgets


class RGBColorField(CharField):
    """Field for database models"""
    widget = widgets.ColorFieldWidget
    default_validators = [RegexValidator(regex=forms.RGB_REGEX)]

    def __init__(self, *args, **kwargs):
        self.colors = kwargs.pop('colors', getattr(settings, 'JS_COLOR_PICKET_COLORS', None))
        self.mode = kwargs.pop('mode', getattr(settings, 'JS_COLOR_PICKET_MODE', None))
        kwargs['max_length'] = 7
        super(RGBColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': forms.RGBColorField,
            'widget': self.widget(mode=self.mode, colors=self.colors),
        })
        return super(RGBColorField, self).formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(RGBColorField, self).deconstruct()
        if self.colors is not None:
            kwargs['colors'] = self.colors
        if self.mode is not None:
            kwargs['mode'] = self.mode
        del kwargs['max_length']
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super(RGBColorField, self).check(**kwargs)
        if self.colors is not None:
            if not isinstance(self.colors, (list, tuple, dict)):
                errors.append(Error(
                    'colors is not iterable',
                    hint='Define the colors param as list of strings(list or dicts) or dict.',
                    obj=self,
                    id='color-picker.E001'
                ))
            else:
                try:
                    if isinstance(self.colors, dict):
                        for color, name in self.colors.items():
                            self.clean(color, None)
                    else:
                        self.colors, tmp = {}, self.colors
                        for el in tmp:
                            if isinstance(el, dict):
                                for color, name in self.colors:
                                    self.clean(color, None)
                                    self.colors[color] = name
                            elif isinstance(el, (tuple, list)):
                                    self.clean(el[0], None)
                                    self.colors[el[0]] = el[1]
                            else:
                                self.clean(el, None)
                                self.colors[el] = el
                except ValidationError:
                    errors.append(Error(
                        'colors item validation error',
                        hint='Each item of the colors param must be a valid '
                             'color string itself.',
                        obj=self,
                        id='color-picker.E002'
                    ))
        return errors
