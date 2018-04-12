from django import forms

from .models import ProjectMeetingPage


class MeetingEditForm(forms.ModelForm):    
    
    class Meta:
        model = ProjectMeetingPage
        fields = ['intro','meeting_notes']
    
    def __init__(self, field_list, *args, **kwargs):    
        super(MeetingEditForm, self).__init__(*args, **kwargs)
        for field in list(self.fields.keys()):
            if field not in field_list:
                del self.fields[field]
