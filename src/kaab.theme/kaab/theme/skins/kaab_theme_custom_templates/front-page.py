## Script (Python) "front-page"
##bind container=container
##bind context=context
##bind script=script
##bind namespace=
##bind subpath=traverse_subpath
##parameters=
##title=
##
# Import a standard function an get the HTML request/response objects:
from Products.PythonScripts.standard import html_quote
request = container.REQUEST
RESPONSE = request.RESPONSE

RESPONSE.redirect(context.portal_url()+'/@@frontpage_view')

