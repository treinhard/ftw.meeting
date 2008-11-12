"""Definition of the Meeting content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from izug.meeting import meetingMessageFactory as _
from izug.meeting.interfaces import IMeeting
from izug.meeting.config import PROJECTNAME

from DateTime.DateTime import DateTime
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.CheckboxColumn import CheckboxColumn

MeetingSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField('location',
                      searchable = True,
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.StringWidget(label = _(u"meeting_label_location", default=u"Event Location"),
                                                  description = _(u"meeting_help_location", default=u"Enter the location where the event will take place."),
                                                  ),
                      ),
                          
    atapi.DateTimeField('start_date',
                        required = True,
                        searchable = True,
                        accessor='start',
                        default_method = DateTime,
                        storage = atapi.AnnotationStorage(),
                        widget = atapi.CalendarWidget(label = _(u"meeting_label_start_date", default=u"Event Starts"),
                                                      description = _(u"meeting_help_start_date", default=u"Enter the starting date and time, or click the calendar icon and select it."),
                                                      ),
                        ),

    atapi.StringField('head_of_meeting',
                      searchable = True,
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.StringWidget(label = _(u"meeting_label_head_of_meeting", default=u"Head of Meeting"),
                                                  description = _(u"meeting_help_head_of_meeting", default=u"Enter the head of the meeting."),
                                                  ),
                      ),
                                          
    atapi.StringField('recording_secretary',
                      searchable = True,
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.StringWidget(label = _(u"meeting_label_recording_secretary", default=u"Recording Secretary"),
                                                  description = _(u"meeting_help_recording_secretary", default=u"Enter the recording secretary."),
                                                  ),
                      ),
                                          
    DataGridField('attendees',
                  searchable = True,
                  columns = ('contact', 'present','excused'),
                  allow_empty_rows = False,
                  storage = atapi.AnnotationStorage(),
                  widget = DataGridWidget(label = _(u"meeting_label_attendees", default=u"Attendees"),
                                          description = _(u"meeting_help_attendees", default=u"Enter the attendees of the meeting."),
                                          auto_insert = True,
                                          columns = {'contact' : Column(label = _(u"meeting_label_attendees_attendee", default=u"Attendee"),
                                                                        ),
                                                     'present' : CheckboxColumn(label = _(u"meeting_label_attendees_present", default=u"Present"),
                                                                                ),
                                                     'excused' : CheckboxColumn(label = _(u"meeting_label_attendees_excused", default=u"Excused"),
                                                                                ),
                                                     }
                                          )
                  ),
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MeetingSchema['title'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(MeetingSchema, folderish=True, moveDiscussion=False)

class Meeting(folder.ATFolder):
    """A type for meetings."""
    implements(IMeeting)

    portal_type = "Meeting"
    schema = MeetingSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    location = atapi.ATFieldProperty('location')
    start_date = atapi.ATFieldProperty('start_date')
    head_of_meeting = atapi.ATFieldProperty('head_of_meeting')
    recording_secretary = atapi.ATFieldProperty('recording_secretary')
    attendees = atapi.ATFieldProperty('attendees')

atapi.registerType(Meeting, PROJECTNAME)