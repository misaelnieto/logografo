import grok
from zope.container.contained import NameChooser
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
        name = NameChooser(self).chooseName(bundle.title, bundle)
        self[name] = bundle

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

class Master(grok.View):
    """
    This is the main macro for consistent look & field
    """
    grok.context(Interface)
