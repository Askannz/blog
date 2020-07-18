#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Gazoche'
SITENAME = "Gazoche's Blog"
SITEURL = 'https://gazoche.xyz'

PATH = 'content'

TIMEZONE = 'Australia/Melbourne'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = [
    ('Pelican', 'http://getpelican.com/'),
    ('Theme: medius', 'https://github.com/onur/medius'),
    ('Python.org', 'http://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/')
]

# Social widget
SOCIAL = []

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "theme/medius"
MEDIUS_AUTHORS = {
    'Gazoche': {
        'image': 'https://gazoche.xyz/images/avatar.png',
        'description': "A random dude",
        'links': [('github', 'https://github.com/Askannz')]
    }
}
