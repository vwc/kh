"""Definition of the Blog Folder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from kaab.blogcontent import blogcontentMessageFactory as _
from kaab.blogcontent.interfaces import IBlogFolder
from kaab.blogcontent.config import PROJECTNAME

BlogFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        name="text",
        searchable=True,
        required=False,
        default_output_type='text/x-html-safe',
        validators=('isTidyHtmlWithCleanup'),
        widget=atapi.RichWidget(
            label=_(u"Text"),
            description=_(u"Enter optional introduction that will be listed "
                          u"above the content listing."),
            allow_file_upload=False,
            rows=15,
            )
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BlogFolderSchema['title'].storage = atapi.AnnotationStorage()
BlogFolderSchema['description'].storage = atapi.AnnotationStorage()
BlogFolderSchema['text'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    BlogFolderSchema,
    folderish=True,
    moveDiscussion=False)


class BlogFolder(folder.ATFolder):
    """A folder holding blogentries"""
    implements(IBlogFolder)

    portal_type = "Blog Folder"
    schema = BlogFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    text = atapi.ATFieldProperty('text')

atapi.registerType(BlogFolder, PROJECTNAME)
