from django import template
from django.db.models import get_apps
from django.core.urlresolvers import reverse
from helpdoc.views import index
import os.path

register = template.Library()

def title(content, site_title=None):
    title = None
    try:
        from BeautifulSoup import BeautifulSoup
        title = BeautifulSoup(content).find("h1")
        if title:
            while True:
                try:
                    title = title.contents[0]
                except (KeyError, AttributeError):
                    break
    except ImportError:
        try:
            from lxml import etree
            parser = etree.HTMLParser()
            title = etree.fromstring(content, parser).xpath("//h1/a")[0].text
        except ImportError:
            pass
    
    if title:
        title = title.encode("UTF-8")
    else:
        title = "Not Found Title Line."
    if site_title and (not title == site_title):
        title += " : %s" % site_title
    return title
register.simple_tag(title)

#def helpdoc_base_url():
#    return reverse(index)
#register.simple_tag(helpdoc_base_url)

def get_app_list():
    app_list = {}
    for app in get_apps():
        if os.path.exists(os.path.join(os.path.dirname(app.__file__), 'docs')):
            app_list[app.__name__.split(".")[-2]] = os.path.dirname(app.__file__)
    return app_list

def app_menu(context):
    context.update(dict(app_list=get_app_list()))
    return context
register.inclusion_tag("tags/app_menu.html", takes_context=True)(app_menu)

def app_list(context):
    context.update(dict(app_list=get_app_list()))
    return context
register.inclusion_tag("tags/app_list.html", takes_context=True)(app_list)

def admin_base_url():
    return reverse('django.contrib.admin.views.main.index')
register.simple_tag(admin_base_url)