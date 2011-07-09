import grok
from zope import interface, schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from logografo import LogografoMessageFactory as _
from logografo.app import Logografo, IDeleteMe
from logografo import resource

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

    end = schema.TextLine(title=_(u'The event ended on this date'),
                          required = False)

    @interface.invariant
    def check_duration(obj):
        if obj.durationEvent and not obj.end:
            raise interface.Invalid(_(u'When adding duration events, you must provide the end date.'))

class HistoryEvent(grok.Model):
    grok.implements(IHistoryEvent, IDeleteMe)
    id = None
    title = None
    description = None
    durationEvent = False
    start = None
    end = None

    def __repr__(self):
        return _(u'History Event (%s)'%self.title)

class Edit (grok.EditForm):
    """
    An EditForm for a HistoryEvent
    Implicit context is HistoryEvent
    """
    def update(self):
        resource.style.need()
        super(Edit, self).update()

    grok.require('logografo.DoAnything')
    template = grok.PageTemplateFile('bundle_templates/add.pt')
    form_fields = grok.AutoFields(HistoryEvent).omit('id')

    def handle_edit_action(self, **data):
        super (Edit, self).handle_edit_action(**data)


def list_bundles(context):
    return SimpleVocabulary([SimpleTerm(b,
                                        token = b.id,
                                        title = b.title) for b in context.values()])

interface.alsoProvides(list_bundles, IContextSourceBinder)

class Add(grok.AddForm):
    """
    An AddForm for a HistoryEvent. Context is an Logografo
    """
    grok.context(Logografo)
    grok.name('add-event')
    grok.require('logografo.DoAnything')
    template = grok.PageTemplateFile('bundle_templates/add.pt')
    form_fields = grok.Fields(
        bundle = schema.Choice(title=_(u'Select event bundle'),
                               description = _(u'Every event must be inside a bundle'),
                               source = list_bundles,
                               required = True)
    ) + grok.AutoFields(HistoryEvent).omit('id')
    label = _(u'Add a History Event')

    def update(self):
        resource.style.need()
        super(Add, self).update()

    @grok.action(_(u'Add'))
    def add(self, **data):
        """
        Action button callback.
        """
        hevent = HistoryEvent()
        self.applyData(hevent, **data)
        bundle = data.get('bundle')
        bundle.addHistoryEvent(hevent)
