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

    def test_event_and_bundle_repr(self):
        obj = EventBundle()
        obj.title = u'hello'
        self.assertEqual(str(obj), u'Event Bundle (hello)')

        obj = HistoryEvent()
        obj.title = u'hello'
        self.assertEqual(str(obj), u'History Event (hello)')

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

        #Master macros
        view = queryMultiAdapter((logografo, TestRequest()), name='master')
        self.assertTrue(view is not None)

        #index
        view = queryMultiAdapter((logografo, TestRequest()), name='index')
        self.assertTrue(view is not None)

        #listing
        view = queryMultiAdapter((logografo, TestRequest()), name='listing')
        self.assertTrue(view is not None)

        #add an EventBundle
        view = queryMultiAdapter((logografo, TestRequest()), name='add-bundle')
        self.assertTrue(view is not None)

        #add a HistoryEvent
        view = queryMultiAdapter((logografo, TestRequest()), name='add-event')
        self.assertTrue(view is not None)

        ##Now test registered views for EventBundle
        eventbundle = EventBundle()

        #edit
        view = queryMultiAdapter((eventbundle, TestRequest()), name='edit')
        self.assertTrue(view is not None)

        #delete
        view = queryMultiAdapter((eventbundle, TestRequest()), name='delete')
        self.assertTrue(view is not None)
        
        #JSON
        view = queryMultiAdapter((eventbundle, TestRequest()), name='json')
        self.assertTrue(view is not None)

        ##Finally, test registered views for HistoryEvent
        historyevent = HistoryEvent()

        #edit
        view = queryMultiAdapter((historyevent, TestRequest()), name='edit')
        self.assertTrue(view is not None)

        #edit
        view = queryMultiAdapter((historyevent, TestRequest()), name='delete')
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
