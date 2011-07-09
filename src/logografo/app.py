import re
import unicodedata

import grok
from zope.container.contained import NameChooser
from zope.container.interfaces import INameChooser
from zope import interface
from logografo import resource
from logografo import LogografoMessageFactory as _

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

class IDeleteMe(interface.Interface):
    """
    Marker interface for objects that accept deletion
    """
    title = interface.Attribute(u'Title of the object')

    def __repr__():
        """ Implementor should render well as string"""

class DeleteObject(grok.Form):
    grok.name('delete')
    grok.context(IDeleteMe)
    grok.require('logografo.DoAnything')
    template = grok.PageTemplateFile('app_templates/delete.pt')
    form_fields = []

    @property
    def label (self):
        return _(u'Do you really want to delete "%s"?'%self.context)

    def update(self):
        resource.style.need()
        super(DeleteObject, self).update()

    @property
    def listing_view(self):
        return self.application_url() + '/@@listing'

    @grok.action(_(u'Cancel'))
    def cancel(self, **data):
        """
        Action button callback.
        """
        self.status = _(u'Delete canceled')
        return self.redirect(self.listing_view)

    @grok.action(_(u'Do it'))
    def doit(self, **data):
        """
        Action button callback.
        """
        del self.context.__parent__[self.context.id]
        self.status = _(u'Delete canceled')
        return self.redirect(self.listing_view)

class IEditable(interface.Interface):
    """
    Marker interface for objects that need an edit form
    """

class EditObject(grok.EditForm):
    """
    An EditForm for a HistoryEvent.
    Implicit context is EventBundle
    """
    grok.context(IEditable)
    grok.name('edit')
    grok.require('logografo.DoAnything')
    template = grok.PageTemplateFile('app_templates/edit.pt')

    #form_fields = grok.AutoFields(EventBundle).omit('id')

    __edit_fields = []
    @property
    def form_fields(self):
        if not self.__edit_fields:
            self.__edit_fields = grok.AutoFields(self.context.__class__).omit('id')
        return self.__edit_fields

    def update(self):
        resource.style.need()
        super(EditObject, self).update()

class Master(grok.View):
    """
    This is the main macro for consistent look & field
    """
    grok.context(interface.Interface)

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
