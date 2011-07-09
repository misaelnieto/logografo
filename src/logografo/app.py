import re
import unicodedata

import grok
from zope.container.contained import NameChooser
from zope.container.interfaces import INameChooser
from zope.interface import Interface
from logografo import resource

class Logografo(grok.Application, grok.Container):
    """
    This is the main Logografo object
    """
    def addBundle(self, bundle):
        """
        Adds a EventBundle to this container.
        """
        name = INameChooser(self).chooseName(bundle.title, bundle)
        bundle.id = name
        self[name] = bundle

    def getContents(self):
        return self.values()

class Index(grok.View):
    """
    Main grok view for Logografo
    """
    def update(self):
        """
        Udate data on grok's view object
        """
        resource.style.need()
        resource.jquery_min.need()
        resource.logografo_timeline.need()
        resource.vtip.need()

class Listing(grok.View):
    """
    Grok view with a list of bundles and history events
    """

    def update(self):
        """
        Udate data on grok's view object
        """
        resource.style.need()
        resource.listing_css.need()
        resource.jquery_min.need()
        resource.listing_js.need()

class Master(grok.View):
    """
    This is the main macro for consistent look & field
    """
    grok.context(Interface)

class ContentNameChooser(grok.Adapter, NameChooser):
    grok.context(grok.Container)
    grok.provides(INameChooser)

    def chooseName(self, name, obj):
        """
         Normalizes string, converts to lowercase, removes non-alpha characters,
         and converts spaces to hyphens.
        """
        # At first choose a name by using Zopes default NameChooser
        name = super(ContentNameChooser, self).chooseName(name, obj)

        #then, normalize
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        name = unicode(re.sub('[^\w\s-]', '', name).strip().lower())
        name = unicode(re.sub('[-\s]+', '-', name))

        # Check the name for errors just to be careful
        self.checkName(name, obj)
        return name
