from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MeetingEditForm

# Create your views here.
def submit_meetingEdit(request, meeting_page, fieldName):

    form = MeetingEditForm(fieldName, data=request.POST or None, instance=meeting_page, label_suffix='')

    if request.method == 'POST' and form.is_valid():      
        
        meeting_page_update = form.save(commit=False)
        meeting_page_update.save_revision().publish()                
        
        return HttpResponseRedirect(meeting_page.url)

    context = {
       'form': form,
       'page': meeting_page,
       'fieldName': fieldName,
    }
    return render(request, 'projects/edit.html', context)