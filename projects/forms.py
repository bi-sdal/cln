from django import forms

from .models import ProjectMeetingPage, ProjectSectionPage, ProjectLiteraturePage
from .models import ProjectDataPage, ProjectAnalysisPage, ProjectPublicationPage
from .models import ProjectMiscPage, ProjectDashboardPage


class MeetingEditForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectMeetingPage
        fields = ['intro','meeting_notes']
    
    def __init__(self, field_list, *args, **kwargs):    
        super(MeetingEditForm, self).__init__(*args, **kwargs)
        for field in list(self.fields.keys()):
            if field not in field_list:
                del self.fields[field]


class LiteratureEditForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectLiteraturePage
        fields = ['intro','literature_notes']
    
    def __init__(self, field_list, *args, **kwargs):    
        super(LiteratureEditForm, self).__init__(*args, **kwargs)
        for field in list(self.fields.keys()):
            if field not in field_list:
                del self.fields[field]


class DataEditForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectLiteraturePage
        fields = ['intro','literature_notes']
    
    def __init__(self, field_list, *args, **kwargs):    
        super(LiteratureEditForm, self).__init__(*args, **kwargs)
        for field in list(self.fields.keys()):
            if field not in field_list:
                del self.fields[field]
                
                
class AnalysisEditForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectLiteraturePage
        fields = ['intro','literature_notes']
    
    def __init__(self, field_list, *args, **kwargs):    
        super(LiteratureEditForm, self).__init__(*args, **kwargs)
        for field in list(self.fields.keys()):
            if field not in field_list:
                del self.fields[field]
                

class PublicationEditForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectLiteraturePage
        fields = ['intro','literature_notes']
    
    def __init__(self, field_list, *args, **kwargs):    
        super(LiteratureEditForm, self).__init__(*args, **kwargs)
        for field in list(self.fields.keys()):
            if field not in field_list:
                del self.fields[field]
                
                
class MiscEditForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectLiteraturePage
        fields = ['intro','literature_notes']
    
    def __init__(self, field_list, *args, **kwargs):    
        super(LiteratureEditForm, self).__init__(*args, **kwargs)
        for field in list(self.fields.keys()):
            if field not in field_list:
                del self.fields[field]
                

class DashboardEditForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectDashboardPage
        fields = ['intro']
    
    def __init__(self, field_list, *args, **kwargs):    
        super(DashboardEditForm, self).__init__(*args, **kwargs)
        for field in list(self.fields.keys()):
            if field not in field_list:
                del self.fields[field]

                
class AddSectionForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectSectionPage
        fields = ['section_name']
