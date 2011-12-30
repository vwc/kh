from zope.interface import implements, Interface

from Acquisition import aq_inner, aq_parent

from DateTime import DateTime

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from plone.memoize.instance import memoize

from kaab.blogcontent import blogcontentMessageFactory as _
from kaab.blogcontent.interfaces import IBlogEntry


class FrontPageView(BrowserView):
    """
    front page browser view
    """
    template = ViewPageTemplateFile('frontpage_view.pt')

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

    @memoize
    def blogentries(self):
        """dict of recently modified blogentries"""
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        return [dict(url=r.getURL(),
                    title=safe_unicode(r.Title),
                    teaser=safe_unicode(r.Description),
                    categories=r.Subject,
                    theme=r.getTheme,
                    image=r.getObject().getImage,
                    comments=r.getObject().talkback.getReplies,
                    modified=self.localize(r.modified))
                for r in catalog(object_provides=IBlogEntry.__identifier__,
                                sort_on='modified',
                                sort_order='reverse',
                                review_state='published')[:6]]

    def localize(self, time):
        """localize the datetime information for modification date"""
        return self._time_localizer()(time.isoformat(),
                                      long_format=True,
                                      context=self.context,
                                      domain='plonelocales')

    @memoize
    def _time_localizer(self):
        """time localizer function"""
        context = aq_inner(self.context)
        translation_service = getToolByName(context, 'translation_service')
        return translation_service.ulocalized_time
