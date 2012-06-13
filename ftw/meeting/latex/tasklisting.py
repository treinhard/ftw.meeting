from Products.CMFCore.utils import getToolByName
from ftw.meeting import meetingMessageFactory
from ftw.meeting.interfaces import IMeeting
from ftw.pdfgenerator.view import MakoLaTeXView
from zope.component import adapts
from zope.i18n import translate
from zope.interface import Interface


class TaskListingLaTeXView(MakoLaTeXView):
    """Adds a task listing to the meeting if ``ftw.task`` is installed.
    This is done by using the post-hook.
    """

    adapts(IMeeting, Interface, Interface)

    template_directories = ['templates']
    template_name = 'tasklisting.tex'

    def __init__(self, *args, **kwargs):
        MakoLaTeXView.__init__(self, *args, **kwargs)
        self.tasks = None

    def render(self):
        self.load_tasks()
        if not self.tasks:
            return ''

        else:
            return MakoLaTeXView.render(self)

    def get_render_arguments(self):
        self.layout.use_package('array,supertabular')

        _ = lambda *a, **kw: translate(
            meetingMessageFactory(*a, **kw), context=self.request)

        return {
            'tasks': self.tasks,

            # Translate here because i18ndude does not find translations
            # in latex templates.
            '_': {
                'pending_tasks': _(u"latex_pending_tasks",
                                   default=u"Pending Tasks"),
                'order': _(u"latex_order", default=u"Order"),
                'responsible': _(u"latex_responsible",
                                 default=u"Responsible"),
                'due_date': _(u"latex_due_date", default=u"Due date"),
                'status': _(u"latex_status", default=u"Status"),
                }}

    def get_related_tasks(self):
        tasks = list(self._get_meeting_tasks()) + list(
            self._get_meeting_item_tasks())

        tasks = list(set(tasks))
        tasks.sort(key=lambda task: task.end())

        return tasks

    def load_tasks(self):
        self.tasks = []

        for task in self.get_related_tasks():
            self.tasks.append({
                    'title': self.convert_plain(task.Title()),
                    'text': self.convert(task.getText()),
                    'responsibility': r'\newline '.join(
                        self._get_names_of_users(task.getResponsibility())),
                    'due_date': self._convert_date(task.end()),
                    'review_state': self._get_review_state(task)})

    def _get_names_of_users(self, usernames):
        names = []

        for username in usernames:
            name = self._get_name_of_user(username)
            names.append(self.convert_plain(name))

        return names

    def _get_name_of_user(self, userid_or_uid):
        acl_users = getToolByName(self.context, 'acl_users')
        user = acl_users.getUserById(userid_or_uid)

        if user and user.getProperty('fullname', ''):
            return user.getProperty('fullname', '')

        elif user:
            return userid_or_uid

        rcatalog = getToolByName(self.context, 'reference_catalog')
        brain = rcatalog.lookupObject(userid_or_uid)
        if brain:
            return brain.Title()

        else:
            return userid_or_uid

    def _convert_date(self, date):
        translation = getToolByName(self.context, 'translation_service')
        localize_time = translation.ulocalized_time
        return localize_time(date, long_format=False)

    def _get_review_state(self, task):
        state_view = task.restrictedTraverse('@@plone_context_state')
        state = state_view.workflow_state()
        return self.convert(translate(state, domain='plone',
                                      context=self.request))

    def _get_meeting_tasks(self):
        for obj in self.context.computeRelatedItems():
            if obj.portal_type == 'Task':
                yield obj

    def _get_meeting_item_tasks(self):
        for item in self.context.getFolderContents(
            {'portal_type': 'Meeting Item'}, full_objects=True):

            for obj in item.computeRelatedItems():
                if obj.portal_type == 'Task':
                    yield obj
