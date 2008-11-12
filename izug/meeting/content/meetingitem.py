"""Definition of the Meeting Item content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from izug.meeting import meetingMessageFactory as _
from izug.meeting.interfaces import IMeetingItem
from izug.meeting.config import PROJECTNAME

MeetingItemSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField('responsibility',
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.StringWidget(label = _(u"meetingitem_label_responsibility", default=u"Responsibility"),
                                                  description = _(u"meetingitem_help_responsibility", default=u"Select the responsible persons."),
                                                  )
                      ),

    atapi.TextField('text',
                    searchable = True,
                    required = False,
                    primary = True,
                    default_content_type = 'text/html',              
                    default_output_type = 'text/html',
                    allowable_content_types = ('text/html','text/structured','text/plain',),
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.RichWidget(label=_(u"meetingitem_label_text", default=u"Text"),
                                              description=_(u"meetingitem_help_text", default=u"Enter the text."),
                                              rows=20,
                                              ),
                    ),

    atapi.StringField('meetingitem_type',
                      vocabulary=((
                                   (u"", u""), 
                                   (u"B", u"resolutions"),
                                   (u"I", u"informations"),
                                   (u"M", u"measures"),
                                   )),
                      enforceVocabulary = True,
                      languageIndependent = True,
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.SelectionWidget(label = _(u"meetingitem_label_item_type", default=u"Item type"),
                                                     description = _(u"meetingitem_help_item_type", default=u"Choose the type of the item."),
                                                     format = 'select',
                                                     ),
                      ),

    atapi.TextField('conclusion',
                    searchable = True,
                    required = False,
                    primary = False,
                    default_content_type = 'text/html',              
                    default_output_type = 'text/html',
                    allowable_content_types = ('text/html','text/structured','text/plain',),
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.RichWidget(label = _(u"meetingitem_label_conclusion", default=u"Conclusion"),
                                              description = _(u"meetingitem_help_conclusion", default=u"Enter the conclusion drawn for this resolution"),
                                              rows=20,
                                              ),
                    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

MeetingItemSchema['title'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(MeetingItemSchema, moveDiscussion=False)

class MeetingItem(folder.ATFolder):
    """A type for meeting items."""
    implements(IMeetingItem)

    portal_type = "Meeting Item"
    schema = MeetingItemSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    responsibility = atapi.ATFieldProperty('responsibility')
    text = atapi.ATFieldProperty('text')
    meetingitem_type = atapi.ATFieldProperty('meetingitem_type')
    conclusion = atapi.ATFieldProperty('conclusion')

atapi.registerType(MeetingItem, PROJECTNAME)