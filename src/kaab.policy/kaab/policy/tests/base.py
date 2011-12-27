from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTextCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup

def setup_kaab_policy():
    """docstring for setup_kaab_policy"""
    fiveconfigure.debug_mode = True
    import kaab.policy
    zcml.load_config('configure.zcml', kaab.policy)
    fiveconfigure.debug_mode = False
    
    ztc.installPackage('kaab.policy')

setup_kaab_policy()
ptc.setupPloneSite(products=['kaab.policy'])

class kaabPolicyTestCase(ptc.PloneTestCase):
    """kaabPolicyTestCase is setup as a base test class"""

        


