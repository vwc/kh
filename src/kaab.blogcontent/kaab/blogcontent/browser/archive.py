from zope.interface import implements, Interface

from Acquisition import aq_inner, aq_parent

from DateTime import DateTime

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from kaab.blogcontent import blogcontentMessageFactory as _
from kaab.blogcontent.interfaces import IBlogEntry


class archiveView(BrowserView):
    """
    archive browser view
    """
    template = ViewPageTemplateFile('archive_view.pt')

    def __call__(self, *args):
        self.theme_filter = self.request.get('theme_filter', None)
        self.subject_filter = self.request.get('subject_filter', None)
        return self.template()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def has_filter(self):
        """test if we have a list of blogentries computed on a given
        filter 'theme_filter' from the request
        """
        return len(self.filtered_blogentries()) > 0

    def has_entries(self):
        """test if matching blogentries exist"""
        return len(self.blogentries()) > 0

    def blogentries(self):
        """return a list of all blogentries listed on modification date"""
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = []
        for r in catalog(object_provides=IBlogEntry.__identifier__,
                            sort_on='modified',
                            sort_order='reverse',
                            review_state='published'):
            results.append(dict(url=r.getURL(),
                                title=r.Title,
                                teaser=r.Description,
                                theme=r.getTheme,
                                categories=r.Subject,
                                image=r.getObject().getImage,
                                comments=r.getObject().talkback.getReplies,
                                modified=self.localize(r.modified)))
        return results

    def filtered_blogentries(self):
        """dict of blogentries filtered by given theme"""
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        return [dict(url=r.getURL(),
                    title=r.Title,
                    teaser=r.Description,
                    categories=r.Subject,
                    theme=r.getTheme,
                    image=r.getObject().getImage,
                    comments=r.getObject().talkback.getReplies,
                    modified=self.localize(r.modified))
                for r in catalog(object_provides=IBlogEntry.__identifier__,
                                    getTheme=self.theme_filter,
                                    sort_on='modified',
                                    sort_order='reverse',
                                    review_state='published')]

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
