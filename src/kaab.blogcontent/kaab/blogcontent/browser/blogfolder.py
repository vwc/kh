from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from plone.memoize.instance import memoize

from kaab.blogcontent.interfaces import IBlogEntry


class blogfolderView(BrowserView):
    """
    blogfolder browser view
    """
    template = ViewPageTemplateFile('blogfolder.pt')

    def __call__(self):
        return self.template()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def has_entries(self):
        """test if matching blogentries exist"""
        return len(self.blogentries()) > 0

    def blogentries(self):
        """return a list of all blogentries in this folder
        sorted on modification date
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = []
        for r in catalog(object_provides=IBlogEntry.__identifier__,
                            path=dict(query='/'.join(
                                        context.getPhysicalPath()),
                                        depth=1),
                            sort_on='modified',
                            sort_order='reverse',
                            review_state='published'):
            results.append(dict(url=r.getURL(),
                                title=safe_unicode(r.Title).encode('utf8'),
                                teaser=r.Description,
                                themes=r.getTheme,
                                categories=r.Subject,
                                image=r.getObject().getImage,
                                comments=r.getObject().talkback.getReplies,
                                modified=self.localize(r.modified)))
        return results

    def localize(self, time):
        """localize the datetime information for modification date"""
        return self._time_localizer()(time,
                                      long_format=False,
                                      context=self.context,
                                      domain='plonelocales')

    @memoize
    def _time_localizer(self):
        """time localizer function"""
        context = aq_inner(self.context)
        translation_service = getToolByName(context, 'translation_service')
        return translation_service.ulocalized_time
