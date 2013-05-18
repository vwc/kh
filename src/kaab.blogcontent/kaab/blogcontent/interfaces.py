from zope import schema
from zope.interface import Interface

from kaab.blogcontent import blogcontentMessageFactory as _

# -*- extra stuff goes here -*-


class IBlogFolder(Interface):
    """A folder holding blogentries"""
    
    title = schema.TextLine(title=(u'Title'),
                            required=True)
    
    description = schema.TextLine(title=_(u'Description'),
                                description=_(u'Enter a short description for this item.'),
                                required=True)
    
    text = schema.SourceText(title=_(u'Text'),
                            description=_(u'Enter optional introduction that will be listed above the content listing.'),
                            required=False)


class IBlogEntry(Interface):
    """A basic blog entry"""
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    
    description = schema.TextLine(title=_(u"Description"),
                                description=_(u"Enter a short summary of this entry that will be shown as a preview."),
                                required=True)
    
    theme = schema.List(title=_(u"Theme"),
                                description=_(u"Select or enter the main theme of this entry."),
                                required=True)
    
    text = schema.SourceText(title=_(u"Text"),
                            description=_(u"Enter the main body text of this blog entry"),
                            required=True)


class IImageProvider(Interface):
    """A interface providing the appropriate html tag"""
    
    tag = schema.TextLine(title=_(u"A HTML tag to render the banner image"))
        