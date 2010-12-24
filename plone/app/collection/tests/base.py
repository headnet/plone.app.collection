import unittest2 as unittest
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import login
from zope.configuration import xmlconfig
from plone.app.testing.layers import FunctionalTesting
from plone.testing import z2
from plone.app.portlets.tests.base import PortletsTestCase


class PACollection(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import plone.app.collection
        xmlconfig.file('configure.zcml', plone.app.collection,
                       context=configurationContext)
        z2.installProduct(app, 'plone.app.collection')

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'plone.app.collection:default')

        # create admin user
        # z2.setRoles(portal, TEST_USER_NAME, ['Manager']) does not work
        # setRoles(portal, TEST_USER_NAME, ['Manager']) is not working either
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')

        # enable workflow for browser tests
        workflow = portal.portal_workflow
        workflow.setDefaultChain('plone_workflow')

        # add a page, so we can test with it
        portal.invokeFactory("Document",
                             "collectiontestpage",
                             title="Collection Test Page")

        # add 6 folders, so we can test with them
        for i in range(6):
            portal.invokeFactory('Folder', 'folder_%s' % i)
        workflow.doActionFor(portal.collectiontestpage, "publish")


PACOLLECTION_FIXTURE = PACollection()

PACOLLECTION_FUNCTIONAL_TESTING =\
                            FunctionalTesting(bases=(PACOLLECTION_FIXTURE,),
                                              name="PACollection:Functional")


class CollectionTestCase(unittest.TestCase):

    layer = PACOLLECTION_FUNCTIONAL_TESTING


class CollectionPortletTestCase(PortletsTestCase):

    layer = PACOLLECTION_FUNCTIONAL_TESTING
