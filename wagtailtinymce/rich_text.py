# Copyright (c) 2016, Isotoma Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Isotoma Limited nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ISOTOMA LIMITED BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import, unicode_literals

import json

from django.forms import widgets
from django.utils import translation
from wagtail.utils.widgets import WidgetWithScript
from wagtail.admin.edit_handlers import RichTextFieldPanel
from wagtail.admin.rich_text.converters.editor_html import DbWhitelister, WhitelistRule
from wagtail.core.whitelist import attribute_rule, check_url
from wagtail.core.rich_text import expand_db_html
from django.conf import settings

allow_without_attributes = attribute_rule({})

class allRules():
    def get(self):
        return True

ELEMENT_RULES = {
    '[document]': allow_without_attributes,
    'a': attribute_rule({'href': check_url}),
    'strong': allow_without_attributes,
    'b': allow_without_attributes,
    'br': allow_without_attributes,
    'div': allow_without_attributes,
    'em': allow_without_attributes,
    'h1': allow_without_attributes,
    'h2': allow_without_attributes,
    'h3': allow_without_attributes,
    'h4': allow_without_attributes,
    'h5': allow_without_attributes,
    'h6': allow_without_attributes,
    'hr': allow_without_attributes,
    'i': allow_without_attributes,
    'img': attribute_rule({'src': check_url, 'width': True, 'height': True,
                           'alt': True}),
    'li': allow_without_attributes,
    'ol': allow_without_attributes,
    'p': allow_without_attributes,
    'strong': allow_without_attributes,
    'sub': allow_without_attributes,
    'sup': allow_without_attributes,
    'table': attribute_rule(allRules),
    'tr': allow_without_attributes,
    'td': allow_without_attributes,
    'th': allow_without_attributes,
}

RULES = []
for k, v in ELEMENT_RULES.items():
    RULES.append(WhitelistRule(k, v))

class TinyMCERichTextArea(WidgetWithScript, widgets.Textarea):

    @classmethod
    def getDefaultArgs(cls):
        return {
            'buttons': [
                [
                    ['undo', 'redo'],
                    ['styleselect'],
                    ['bold', 'italic'],
                    ['bullist', 'numlist', 'outdent', 'indent'],
                    ['table'],
                    ['link', 'unlink'],
                    ['wagtaildoclink', 'wagtailimage', 'wagtailembed'],
                    ['pastetext', 'fullscreen'],
                ]
            ],
            'menus': False,
            'options': {
                'browser_spellcheck': True,
                'noneditable_leave_contenteditable': True,
                'language': translation.to_locale(translation.get_language()),
                'language_load': True,
            },
        }

    def __init__(self, attrs=None, **kwargs):
        translation.trans_real.activate(settings.LANGUAGE_CODE)
        super(TinyMCERichTextArea, self).__init__(attrs)
        self.kwargs = self.getDefaultArgs()
        if kwargs is not None:
            self.kwargs.update(kwargs)

    def get_panel(self):
        return RichTextFieldPanel

    def render(self, name, value, attrs=None):
        if value is None:
            translated_value = None
        else:
            translated_value = expand_db_html(value)#, for_editor=True)
        return super(TinyMCERichTextArea, self).render(name, translated_value, attrs)

    def render_js_init(self, id_, name, value):
        kwargs = {
            'options': self.kwargs.get('options', {}),
        }

        if 'buttons' in self.kwargs:
            if self.kwargs['buttons'] is False:
                kwargs['toolbar'] = False
            else:
                kwargs['toolbar'] = [
                    ' | '.join([' '.join(groups) for groups in rows])
                    for rows in self.kwargs['buttons']
                ]

        if 'menus' in self.kwargs:
            if self.kwargs['menus'] is False:
                kwargs['menubar'] = False
            else:
                kwargs['menubar'] = ' '.join(self.kwargs['menus'])

        return "makeTinyMCEEditable({0}, {1});".format(json.dumps(id_), json.dumps(kwargs))

    def value_from_datadict(self, data, files, name):
        original_value = super(TinyMCERichTextArea, self).value_from_datadict(data, files, name)
        if original_value is None:
            return None
        dbw = DbWhitelister(RULES.copy())
        print(dbw.element_rules)
        return dbw.clean(original_value)
