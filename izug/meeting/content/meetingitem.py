"""Definition of the Meeting Item content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner, aq_parent

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.CMFCore.utils import getToolByName

from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime

from izug.arbeitsraum.content.utilities import finalizeIzugSchema

from izug.meeting import meetingMessageFactory as _
from izug.meeting.interfaces import IMeetingItem
from izug.meeting.config import PROJECTNAME

MeetingItemSchema = folder.ATFolderSchema.copy() + atapi.Schema((

     atapi.LinesField('responsibility',
                      required = False,
                      searchable = True,
                      index = 'KeywordIndex:schema',               
                      vocabulary = 'getAssignableUsers',
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.MultiSelectionWidget(size = 4,
                                                          label = _(u"meetingitem_label_responsibility", default=u"Responsibility"),
                                                          description = _(u"meetingitem_help_responsibility", default=u"Select the responsible person(s)."),
                                                          format='checkbox',
                                                          ),
                      ),

    atapi.TextField('text',
                    searchable = True,
                    required = False,
                    primary = True,
                    default_content_type = 'text/html',
                    default_output_type = 'text/html',
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.RichWidget(label=_(u"meetingitem_label_text", default=u"Text"),
                                              description=_(u"meetingitem_help_text", default=u"Enter the text."),
                                              rows=10,
                                              ),
                    ),


    atapi.TextField('conclusion',
                    searchable = True,
                    required = False,
                    primary = False,
                    default_content_type = 'text/html',              
                    default_output_type = 'text/html',
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.RichWidget(label = _(u"meetingitem_label_conclusion", default=u"Conclusion"),
                                              description = _(u"meetingitem_help_conclusion", default=u"Enter the conclusion drawn for this resolution"),
                                              rows=10,
                                              ),
                    ),

    atapi.ReferenceField('related_items',
                         relationship = 'relatesTo',
                         multiValued = True,
                         isMetadata = True,
                         languageIndependent = False,
                         index = 'KeywordIndex',
                         accessor = 'relatedItems',
                         storage = atapi.AnnotationStorage(),
                         schemata = 'default',
                         widget = ReferenceBrowserWidget(
                                                         allow_search = True,
                                                         allow_browse = True,
                                                         show_indexes = False,
                                                         force_close_on_insert = True,
                                                         label = _(u"meetingitem_label_related_items", default=u"Related Items"),
                                                         description = _(u"meetingitem_help_related_items", default=u""),
                                                         visible = {'edit' : 'visible', 'view' : 'invisible' }
                                                         ),
                         ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

MeetingItemSchema['title'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}


finalizeIzugSchema(MeetingItemSchema, moveDiscussion=False)

MeetingItemSchema.changeSchemataForField('effectiveDate','settings')
MeetingItemSchema.changeSchemataForField('expirationDate','settings')
MeetingItemSchema['effectiveDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}
MeetingItemSchema['expirationDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}

class MeetingItem(folder.ATFolder):
    """A type for meeting items."""
    implements(IMeetingItem)

    portal_type = "Meeting Item"
    schema = MeetingItemSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    duration = atapi.ATFieldProperty('duration')
    responsibility = atapi.ATFieldProperty('responsibility')
    text = atapi.ATFieldProperty('text')
    meetingitem_type = atapi.ATFieldProperty('meetingitem_type')
    conclusion = atapi.ATFieldProperty('conclusion')
    related_items = atapi.ATFieldProperty('related_items')

    def getAssignableUsers(self):
        """Collect users with a given role and return them in a list.
        """
        role = 'Reader'
        results = []
        pas_tool = getToolByName(self, 'acl_users')
        utils_tool = getToolByName(self, 'plone_utils')

        for user_id_and_roles in utils_tool.getInheritedLocalRoles(self):
            if user_id_and_roles[2] == 'user':
                if role in user_id_and_roles[1]:
                    user = pas_tool.getUserById(user_id_and_roles[0])
                    if user:
                        results.append((user.getId(), '%s (%s)' % (user.getProperty('fullname', ''), user.getId())))
            if user_id_and_roles[2] == 'group':
                if role in user_id_and_roles[1]:
                    for user in pas_tool.getGroupById(user_id_and_roles[0]).getGroupMembers():
                        results.append((user.getId(), '%s (%s)' % (user.getProperty('fullname', ''), user.getId())))
                
        return (atapi.DisplayList(results))

    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

atapi.registerType(MeetingItem, PROJECTNAME)
