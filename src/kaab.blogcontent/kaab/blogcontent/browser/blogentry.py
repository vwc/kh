from zope.interface import implements, Interface

from Acquisition import aq_inner, aq_parent
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from kaab.blogcontent.interfaces import IBlogEntry
from kaab.blogcontent.interfaces import IImageProvider
from kaab.blogcontent import blogcontentMessageFactory as _


class BlogEntryView(BrowserView):
    """
    blogentry browser view
    """
    template = ViewPageTemplateFile('blogentry.pt')

    def __call__(self):
        return self.template()

    def image_tag(self):
        context = aq_inner(self.context)
        image_provider = IImageProvider(context)
        return image_provider.tag

    def filed_under(self):
        """query the parent blogfolder and make this information
        accessable"""
        context = aq_inner(self.context)
        parent = aq_parent(aq_inner(context))
        return [dict(title=parent.title,
                    url=parent.absolute_url())]
