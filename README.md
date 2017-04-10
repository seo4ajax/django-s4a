Django-s4a
=============

[SEO4Ajax](https://www.seo4ajax.com) is a service that let you get full visibility on search engines, social networks and display advertising of any AJAX website based on Angular, React, Backbone, Ember, jQuery etc.

django-s4a is a middleware for Django. It provides an easy way to
proxify GET requests from non-js clients (e.g. crawlers) to [SEO4Ajax](https://www.seo4ajax.com).

Usage
-----

Copy the seo4ajax.py file in your project root.

Add the middleware in the `MIDDLEWARE` list in settings.py, e.g. 

    MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
      'project.seo4ajax.Middleware'
    ]
    
Set the `S4A_TOKEN` environment variable with the SEO4Ajax token of your site.

How it works
------------

This middleware checks the presence of the _escaped_fragment_ query parameter or the presence of a user-agent string identifying bots that do not support the Ajax Crawling Specification.
If the _escaped_fragment_ is present or a bot is detected, it requests the snapshot on SEO4Ajax and responds to the initial request with the concerned snapshot.


Requirements
------------

- requests (http://docs.python-requests.org/en/master/)


