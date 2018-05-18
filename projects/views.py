from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *

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
    

def submit_literatureEdit(request, literature_page, fieldName):

    form = LiteratureEditForm(fieldName, data=request.POST or None, instance=literature_page, label_suffix='')

    if request.method == 'POST' and form.is_valid():      
        
        literature_page_update = form.save(commit=False)
        literature_page_update.save_revision().publish()                
        
        return HttpResponseRedirect(literature_page.url)

    context = {
       'form': form,
       'page': literature_page,
       'fieldName': fieldName,
    }
    return render(request, 'projects/edit.html', context)
    
    
def submit_dataEdit(request, data_page, fieldName):

    form = DataEditForm(fieldName, data=request.POST or None, instance=data_page, label_suffix='')

    if request.method == 'POST' and form.is_valid():      
        
        data_page_update = form.save(commit=False)
        data_page_update.save_revision().publish()                
        
        return HttpResponseRedirect(data_page.url)

    context = {
       'form': form,
       'page': data_page,
       'fieldName': fieldName,
    }
    return render(request, 'projects/edit.html', context)
    
    
def submit_analysisEdit(request, analysis_page, fieldName):

    form = AnalysisEditForm(fieldName, data=request.POST or None, instance=analysis_page, label_suffix='')

    if request.method == 'POST' and form.is_valid():      
        
        analysis_page_update = form.save(commit=False)
        analysis_page_update.save_revision().publish()                
        
        return HttpResponseRedirect(analysis_page.url)

    context = {
       'form': form,
       'page': analysis_page,
       'fieldName': fieldName,
    }
    return render(request, 'projects/edit.html', context)
    
    
def submit_publicationEdit(request, publication_page, fieldName):

    form = PublicationEditForm(fieldName, data=request.POST or None, instance=publication_page, label_suffix='')

    if request.method == 'POST' and form.is_valid():      
        
        publication_page_update = form.save(commit=False)
        publication_page_update.save_revision().publish()                
        
        return HttpResponseRedirect(publication_page.url)

    context = {
       'form': form,
       'page': publication_page,
       'fieldName': fieldName,
    }
    return render(request, 'projects/edit.html', context)
    
    
def submit_miscEdit(request, misc_page, fieldName):

    form = MiscEditForm(fieldName, data=request.POST or None, instance=misc_page, label_suffix='')

    if request.method == 'POST' and form.is_valid():      
        
        misc_page_update = form.save(commit=False)
        misc_page_update.save_revision().publish()                
        
        return HttpResponseRedirect(misc_page.url)

    context = {
       'form': form,
       'page': misc_page,
       'fieldName': fieldName,
    }
    return render(request, 'projects/edit.html', context)
    

def submit_dashboardEdit(request, page, fieldName):

    form = DashboardEditForm(fieldName, data=request.POST or None, instance=page, label_suffix='')

    if request.method == 'POST' and form.is_valid():      
        
        page_update = form.save(commit=False)
        page_update.save_revision().publish()                
        
        return HttpResponseRedirect(page.url)

    context = {
       'form': form,
       'page': page,
       'fieldName': fieldName,
    }
    return render(request, 'projects/edit.html', context)

    
def submit_sectionAdd(request, current_page):

    form = AddSectionForm(data=request.POST or None, label_suffix='')

    if request.method == 'POST' and form.is_valid():      
        
        section_page = form.save(commit=False)
        section_page.title = section_page.section_name
        current_page.add_child(instance=section_page)
        section_page.save_revision().publish()                
        
        return HttpResponseRedirect(current_page.url)

    context = {
       'form': form,
       'current_page': current_page,
    }
    return render(request, 'projects/sectionAdd.html', context)