from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render

from wagtail.core.models import Page
from project_structure.models import *
from projects.models import *

# Create your views here.
class ResearcherCreate(CreateView):
    model = Researcher
    fields = [
        'first_name', 
        'last_name',
        'degree',
        'email',
        'website',
        ]

class ResearcherUpdate(UpdateView):
    model = Researcher
    fields = [
        'first_name', 
        'last_name',
        'degree',
        'email',
        'website',
        ]

class ResearcherDelete(DeleteView):
    model = Researcher
    success_url = reverse_lazy('researcher-list')
    

class ResearcherDetail(DetailView):
    model = Researcher
    context_object_name = 'researcher'
    
class ResearcherList(ListView):
    model = Researcher


# Project Views    
class ProjectCreate(CreateView):
    model = Project
    fields = ['title', 'acronym', 'researchers', 'git_repo', 'shared_drive']    
    
    def form_valid(self, form):
        self.object = form.save()

        print (form)        
        
        #Add Page to Notebook
        page = ProjectDashboardPage(title=form.cleaned_data['title'], project_structure = self.object)      

        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        page.save_revision().publish()

        return render(self.request, 'project_structure/project_detail.html', {'project': self.object})


class ProjectUpdate(UpdateView):
    model = Project
    fields = '__all__'

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project-list')
    

class ProjectDetail(DetailView):
    model = Project
    context_object_name = 'project'
    
class ProjectList(ListView):
    model = Project
    
    
# Meeting Views
class MeetingCreate(CreateView):
    model = Meeting
    fields = ['date', 'prepared_by', 'project_attendees']   
            
    def form_valid(self, form):
        projectId = self.kwargs['project']
        project = Project.objects.get(id=projectId)                
        
        self.object = form.save()
        self.object.project = project
        self.object.save()
        
        page = ProjectMeetingPage(title='Meeting-{}'.format(self.object.date), meeting_structure = self.object)
        
        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        
        page.save_revision().publish() 

        return render(self.request, 'project_structure/meeting_detail.html', {'meeting': self.object})

class MeetingUpdate(UpdateView):
    model = Meeting
    fields = '__all__'

class MeetingDelete(DeleteView):
    model = Meeting
    success_url = reverse_lazy('meeting-list')
    
class MeetingDetail(DetailView):
    model = Meeting
    context_object_name = 'meeting'
    
class MeetingList(ListView):
    model = Meeting
    
