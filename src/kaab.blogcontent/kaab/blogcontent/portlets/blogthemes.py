from zope.interface import Interface
from zope.interface import implements

from Acquisition import aq_inner, aq_parent

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from kaab.blogcontent import blogcontentMessageFactory as _

class IBlogThemes(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IBlogThemes)


    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Themes")


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('blogthemes.pt')
    
    def themes(self):
        results = self._getThemesSorted()
        return results
    
    def _getThemesSorted(self):
        """query the catalog and assemble a list of available themes
        for blogentries
        """
        context = aq_inner(self.context)
        self.catalog = getToolByName(context, 'portal_catalog')
        themes = list(self.catalog.uniqueValuesFor('getTheme'))
        if themes:
            themes.sort(lambda x, y: cmp(x.lower(), y.lower()))
        return tuple(themes)


class AddForm(base.NullAddForm):
    """Portlet add form - inherit from NullAddForm to remove all configuration
    """

    def create(self):
        return Assignment()

