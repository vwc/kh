"""Definition of the BlogEntry content type
"""

from zope.interface import implements
from zope.component import adapts

from Products.Archetypes import atapi
from Products.validation import V_REQUIRED

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from kaab.blogcontent import blogcontentMessageFactory as _
from kaab.blogcontent.interfaces import IBlogEntry
from kaab.blogcontent.interfaces import IImageProvider
from kaab.blogcontent.config import PROJECTNAME

BlogEntrySchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.LinesField(
        name='theme',
        searchable=True,
        widget=atapi.KeywordWidget(
            label=_(u'Theme'),
            description=_(u'Select or enter the main theme of this entry.')
        )
    ),


    atapi.TextField(
        name='text',
        searchable=True,
        allowable_content_types=('text/html',),
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u"Text"),
            description=_(u"Enter the main body text of this blog entry"),
            allow_file_upload=False,
            rows=25,
        ),
        required=True,
    ),
    atapi.ImageField('image',
        languageIndependent=True,
        swallowResizeExceptions=True,
        sizes={'large': (768, 768),
               'preview': (450, 450),
               'mini': (200, 200),
               'thumb': (128, 128),
               'tile': (64, 64),
               'icon': (32, 32),
               'listing': (16, 16),
               },
        validators=(('isNonEmptyFile', V_REQUIRED),
                    ('checkImageMaxSize', V_REQUIRED)),
        widget=atapi.ImageWidget(label=_(u"Preview Image"),
                                description=_(u"Upload an image that will be "
                                    u"shown as a preview image in listings."),
                                show_content_type=False,),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

BlogEntrySchema['title'].storage = atapi.AnnotationStorage()
BlogEntrySchema['description'].storage = atapi.AnnotationStorage()
BlogEntrySchema['theme'].storage = atapi.AnnotationStorage()
BlogEntrySchema['text'].storage = atapi.AnnotationStorage()
BlogEntrySchema['image'].storage = atapi.AnnotationStorage()


schemata.finalizeATCTSchema(BlogEntrySchema, moveDiscussion=False)


class BlogEntry(base.ATCTContent):
    """A basic blog entry"""
    implements(IBlogEntry)

    portal_type = "BlogEntry"
    schema = BlogEntrySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    theme = atapi.ATFieldProperty('theme')
    text = atapi.ATFieldProperty('text')
    # Borrow the relevant methods to render scaled images
    # in folder listings from ATContentType's ATNewsItem class

    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField"""
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """ Enable access to /path/image_<scalename> by copying from
            ATNewsItem
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                return image
        return super(BlogEntry, self).__bobo_traverse__(REQUEST, name)


atapi.registerType(BlogEntry, PROJECTNAME)

# Test implementation that uses an adapter to extract the
# corresponding html tag for our image field:


class ImageProvider(object):
    """ImageProvider returning the appropriate html tag"""
    implements(IImageProvider)
    adapts(BlogEntry)

    def __init__(self, context):
        self.context = context

    @property
    def tag(self):
        """docstring for tag"""
        return self.context.getField('image').tag(self.context, scale='large')
