import grok

from zope import interface, schema
from zope.container.interfaces import INameChooser

from logografo import LogografoMessageFactory as _
from logografo import resource
from logografo.app import Logografo, IDeleteMe, IEditable

class IEventBundle(interface.Interface):
    """
    Event Bundle only has
    """
    id = schema.ASCIILine(title = u'id',
                          required = False)

    title = schema.TextLine(title = _(u'Title'),
                            description= _(u'Give a title to this Bundle, for example: "Scientific discoveries"'),
                            required = True)

    description = schema.Text(title = _(u'Just a brief description of this bundle'),
                              required= False)

    def getContents():
        """
        Returns a list of all events contained in this bundle
        """


class EventBundle(grok.Container):
    """
    This is an Event bundle that will group HistoryEvents
    """
    grok.implements(IEventBundle, IDeleteMe, IEditable)

    id = None
    title = None
    description = None

    def addHistoryEvent(self, hevent):
        """
        Adds a HistoryEvent to this container.
        """
        name = INameChooser(self).chooseName(hevent.title, hevent)
        hevent.id = name
        self[name] = hevent

    def getContents(self):
        return self.values()

    def __repr__(self):
        return _(u'Event Bundle (%s)'%self.title)

class Add(grok.AddForm):
    """
    An AddForm for a EventBundle
    """
    grok.context(Logografo)
    grok.name('add-bundle')
    grok.require('logografo.DoAnything')
    form_fields = grok.AutoFields(IEventBundle).omit('id')
    template = grok.PageTemplateFile('bundle_templates/add.pt')
    label = _(u'Add a bundle of events')

    def update(self):
        resource.style.need()
        super(Add, self).update()

    @grok.action(_(u'Add Bundle'))
    def add (self, **data):
        bundle = EventBundle()
        self.applyData(bundle, **data)
        self.context.addBundle(bundle)
        return self.redirect(self.url(self.context))

class EventsDataJson(object):
    wikiURL = None
    wikiSection = None
    dateTimeFormat = None
    
    def __init__(self, data, 
                 wikiURL = None, wikiSection = None, 
                 dateTimeFormat= None):
        self.data = data
        self.wikiURL = wikiURL
        self.wikiSection = wikiSection
        self.dateTimeFormat = dateTimeFormat


class Serialize(grok.JSON):
    """
    Json representation of event bundle
    """
    def json(self):
        return {'wikiURL': 'https://github.com/tzicatl/logografo',
                'dateTimeFormat': 'Gregorian',
                'events': [{'title': h.title,
                            'description' : h.description,
                            'durationEvent' : h.durationEvent,
                            'start' : h.start,
                            'end' : h.end} for h in self.context.getContents()]
                }
    