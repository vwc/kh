from zope.interface import Interface
from zope.interface import implements

from Acquisition import aq_inner, aq_parent

from plone.app.portlets.portlets import base
from plone.app.portlets.cache import render_cachekey

from plone.portlets.interfaces import IPortletDataProvider

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize

from zope import schema
from zope.formlib import form
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from kaab.blogcontent import blogcontentMessageFactory as _

class IBlogArchive(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    count = schema.Int(title=_(u"Number of blogentries to display"),
                        description=_(u"Please specify haw many blog entries from the archive this portlet shoul query."),
                        required=True,
                        default=6)



class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IBlogArchive)

    def __init__(self, count=6):
        self.count = count

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Archive")

def _render_cachekey(fun, self):
    """render the necessary cachekey"""
    return render_cachekey(fun, self)

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('blogarchive.pt')
    
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.catalog = plone_tools.catalog()
        self.typesToShow = ('BlogEntry',)
    
    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())
    
    @property
    def available(self):
        """test if we have data available"""
        return len(self._data())
    
    def recent_entries(self):
        """make our results available"""
        return self._data()
    
    def recently_modified_link(self):
        """add a link to the blogentry archive"""
        return '%s/archive_view' % self.portal_url
    
    @memoize
    def _data(self):
        limit = self.data.count
        return self.catalog(portal_type=self.typesToShow,
                            sort_on='modified',
                            review_state='published',
                            sort_order='reverse',
                            sort_limit=limit)[:limit]



class AddForm(base.AddForm):

    form_fields = form.Fields(IBlogArchive)
    label=_(u"Add Recent BlogEntries Portlet")
    description=_(u"This portlet will display a configurable number of recently modified blogentries.")

    def create(self, data):
        return Assignment(count=data.get('limit', 6))


class EditForm(base.EditForm):
    """Portlet edit form."""
    
    form_fields = form.Fields(IBlogArchive)
    label=_(u"Edit Recent BlogEntries Portlet")
    description =_(u"Configure how many recently modified blogentries this portlet will display.")
    
