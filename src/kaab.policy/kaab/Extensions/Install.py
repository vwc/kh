import transaction
from Products.CMFCore.utils import getToolByName

EXTENSION_PROFILES =
PRODUCT_DEPENDENCIES =

def install(self, reinstall=False):
	"""custom install method for the extension profile"""
	portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
	portal_setup =getToolByName(self, 'portal_setup')
	
	for product in PRODUCT_DEPENDENCIES:
		if reinstall and portal_quickinstaller(isProductInstalled(product):
			portal_quickinstaller.reinstallProducts([product])
			transaction.savepoint()
		elif not portal_quickinstaller.isProductInstalled(product):
			portal_quickinstaller.installProduct(product)
			transaction.savepoint()
	
	for extension_id in EXTENSION_PROFILES:
		portal_setup.runAllStepsFromProfile('profile-%s' % extension_id, purge_old=False)
		product_name = extension_id.split(':')[0]
		portal_quickinstaller.notifyInstalled(product_name)
		transaction.savepoint()

