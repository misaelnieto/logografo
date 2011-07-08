import unittest
import datetime

from zope import interface, schema
from zope.component import queryAdapter, queryMultiAdapter
from zope.publisher.browser import TestRequest

from zope.fanstatic.testing import ZopeFanstaticBrowserLayer

import logografo.tests
from logografo.app import Logografo
from logografo.historyevent import HistoryEvent, IHistoryEvent
from logografo.bundle import EventBundle

# In this file we create a unittest, a functional unittest.

class MyTestCase(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(1, 1)

browser_layer = ZopeFanstaticBrowserLayer(logografo.tests)

class MyFunctionalTestCase(unittest.TestCase):

    layer = browser_layer

    def test_name_chooser(self):
        """
        Test the namechooser adapter
        """
        from zope.container.interfaces import INameChooser
        logografo = Logografo()
        logografo['foobar.old'] = 'rst doc'
        logografo['derp'] = 'rst doc'
        logografo['derp-1'] = 'rst doc'
        logografo['derp-2'] = 'rst doc'


        chooser = queryAdapter(logografo, INameChooser)
        self.assertTrue(chooser is not None)

        self.assertEqual(chooser.chooseName(u'foo', object()),
                         u'foo')
        self.assertEqual(chooser.chooseName(u'foobar.old', object()),
                         u'foobar-2old')
        self.assertEqual(chooser.chooseName(u'derp', object()),
                         u'derp-3')
        self.assertEqual(chooser.chooseName(u'@@sanitize-me@@', object()),
                         u'sanitize-me')
        self.assertEqual(chooser.chooseName(u'++sanitize-me++', object()),
                         u'sanitize-me')
        self.assertEqual(chooser.chooseName(u'Something with spaces', object()),
                         u'something-with-spaces')
        self.assertEqual(chooser.chooseName(u'international: \xe1\xe9\xed\xf3\xfa\u011d\u0125', object()),
                         u'international-aeiough')

    def test_views_are_registered(self):
        """
        Test availability of views
        """

        ##Test registered views for Logografo
        logografo = Logografo()

        #index
        view = queryMultiAdapter((logografo, TestRequest()), name='index')
        self.assertTrue(view is not None)

        #add a bundle
        view = queryMultiAdapter((logografo, TestRequest()), name='add')
        self.assertTrue(view is not None)

        ##Now test registered views for EventBundle
        eventbundle = EventBundle()

        #view -- eventbundle does not have edit view -should it have?
        view = queryMultiAdapter((eventbundle, TestRequest()), name='index')
        self.assertTrue(view is None)

        #add
        view = queryMultiAdapter((eventbundle, TestRequest()), name='add')
        self.assertTrue(view is not None)

        #edit
        view = queryMultiAdapter((eventbundle, TestRequest()), name='edit')
        self.assertTrue(view is not None)

        ##Finally, test registered views for HistoryEvent
        historyevent = HistoryEvent()

        #index
        view = queryMultiAdapter((historyevent, TestRequest()), name='index')
        self.assertTrue(view is not None)

        #edit
        view = queryMultiAdapter((historyevent, TestRequest()), name='edit')
        self.assertTrue(view is not None)


    def test_historyevent_invariant(self):
        """
        Exercise the different validation options fo HistoryEvent Objects.
        """

        #Duration events with no end date are invalid
        hevent = HistoryEvent()
        hevent.title = u'95th World Congress of Esperanto'
        hevent.durationEvent = True
        hevent.start = u'Jul 17 2010 00:00:00 GMT-0600'
        errors = schema.getValidationErrors(IHistoryEvent, hevent)
        self.assertGreater(len(errors), 0)

        #adding the missing piece of data makes the validator happy
        hevent.end = u'JFeb 11 2012 00:00:00 GMT-0600'
        errors = schema.getValidationErrors(IHistoryEvent, hevent)
        self.assertEqual(len(errors), 0)
