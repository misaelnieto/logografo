import grok
from zope import interface, schema

from logografo import LogografoMessageFactory as _
from logografo.bundle import EventBundle

class IHistoryEvent(interface.Interface):
    """
    Schema for a History event
    """
    id = schema.ASCIILine(title = u'id',
                          required = False)

    title = schema.TextLine(title = _(u'Title'),
                            description= _(u'Write a title for the Historic Event'),
                            required = True)

    description = schema.Text(title = _(u'Brief description of the event'),
                              required = False)

    durationEvent = schema.Bool(title=_(u'Should the event have a duration?'),
                           description = _(u'Events that have a duration must specify an end date'),
                           required = True)

    start = schema.TextLine(title=_(u'Event date'),
                            description=_(u'This is the date of the event (or when the event started)'),
                            required = True)

    end = schema.TextLine(title=_(u'The event ended on this date'))

    @interface.invariant
    def check_duration(obj):
        if obj.durationEvent and not obj.end:
            raise interface.Invalid(_(u'When adding duration events, you must provide the end date.'))


def isValidEvent(data):
    """
    Verifies if the event data is valid.

    Events are dictionaries with some mandatory and optional entries.

    Mandatory entries are:

    - title
    - durationEvent
    - start
    - end (Only mandatory if durationEvent is True

    Optional entries are

    - description
    - Any other I cannot think of right now.
    """
    if isinstance(data, dict):
        mandatory = ['title', 'durationEvent', 'start']
        conditional = ['end']
        mpoints = sum(map(lambda x: x in data.keys(), mandatory))
        cpoints = sum(map(lambda x: x in data.keys(), conditional))
        if mpoints == len(mandatory):
            if data['durationEvent']:
                return cpoints == len(conditional)
            return True
    return False

class HistoryEvent(grok.Model):
    grok.implements(IHistoryEvent)
    id = None
    title = None
    description = None
    durationEvent = False
    start = None
    end = None

class Index(grok.DisplayForm):
    """
    This view makes it possible to view a single history event.
    """
    form_fields  = grok.AutoFields(HistoryEvent)

class Edit (grok.EditForm):
    """
    An EditForm for a HistoryEvent
    Implicit context is HistoryEvent
    """
    template = grok.PageTemplateFile('bundle_templates/add.pt')
    form_fields = grok.AutoFields(HistoryEvent)

class Add(grok.AddForm):
    """
    An AddForm for a HistoryEvent. Context is an Eventbundle
    """
    grok.context(EventBundle)
    template = grok.PageTemplateFile('bundle_templates/add.pt')
    form_fields = grok.AutoFields(HistoryEvent)
    label = _(u'Add a History Event')

    @grok.action(_(u'Add'))
    def add(self, **data):
        """
        Action button callback.
        """
        hevent = HistoryEvent()
        self.applyData(hevent, **data)
        self.context.addHistoryEvent(hevent)
