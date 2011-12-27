import unittest
from kaab.policy.test.base import kojaPolicyTestCase

from Products.CMFCore.utils import getToolByName

class TestSetup(kojaPolicyTestCase):
    """initialize Test Setup"""
    
    def test_portal_title(self):
        """docstring for test_portal_title"""
        self.assertEquals("Informationsdesign Katharina Hölzl", self.portal.getProperty('title'))
    
    def test_portal_description(self):
        """docstring for test_portal_description"""
        self.assertEquals("transformation into space", self.portal.getProperty('description'))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeTestSuite(TestSetup))
    return suite
        

