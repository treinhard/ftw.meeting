from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class GenerateMeetingViewlet(ViewletBase):
    """Shows a "generate meeting from poodle" button

    """
    render = ViewPageTemplateFile('generate_meeting.pt')

    def update(self):
        """define some values to grap from template"""

        poodle_table = self.context.restrictedTraverse('@@ftw_poodle_table')
        if not poodle_table:
            # ok poodle is not available
            return

        # raw result from poodletable
        # includes a new part results (counted votes per date entry)
        self.poodle_result = poodle_table.poodleResults(print_html=False)

        # dict which containes
        options_list = []
        # first iterate throught dates - for the right order
        for i, date in enumerate(self.poodle_result['dates']):
            # dates_record is the correct entry from getDates(datagridfield)
            dates_record = self.context.getDates()[i]
            options_list.append(
                dict(
                    hash=self.poodle_result['ids'][i],
                    date=dates_record['date'],
                    duration=dates_record['duration'],
                    counter=self.poodle_result['result'][i]))

        self.options = options_list
