from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect

from wagtail.core.models import Page
from django.contrib.auth.models import User
from project_structure.models import *
from projects.models import *

# Create your views here.
class NoteAdd(TemplateView):
    
    template_name = "project_structure/list_add_sections.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent = ProjectDashboardPage.objects.get(pk=context['pk'])
        context['sections'] = ProjectSectionPage.objects.child_of(parent).live()
        return context 
    

# Researcher Bits
class ResearcherCreate(CreateView):
    model = Researcher
    fields = [
        'user',
        'first_name', 
        'last_name',
        'degree',
        'email',
        'website',
        'description',
        ]
    success_url = reverse_lazy('researcher-list')
    
    def get_initial(self):
        uid = self.kwargs.get('userId', None)
        if (uid):
            user = User.objects.get(username=uid)
            return {
                'user': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }


class ResearcherUpdate(UpdateView):
    model = Researcher
    fields = [
        'first_name', 
        'last_name',
        'degree',
        'email',
        'website',
        'description',
        ]

class ResearcherDelete(DeleteView):
    model = Researcher
    success_url = reverse_lazy('researcher-list')
    

class ResearcherDetail(DetailView):
    model = Researcher
    context_object_name = 'researcher'
    
class ResearcherList(ListView):
    model = Researcher


#Sponsor Bits
class SponsorCreate(CreateView):
    model = Sponsor
    fields = [
        'user',
        'first_name', 
        'last_name',
        'organization',
        'title',
        'email',
        'website',
        'org_description',
        ]
    success_url = reverse_lazy('sponsor-list')

class SponsorUpdate(UpdateView):
    model = Sponsor
    fields = [
        'first_name', 
        'last_name',
        'organization',
        'title',
        'email',
        'website',
        'org_description',
        ]

class SponsorDelete(DeleteView):
    model = Sponsor
    success_url = reverse_lazy('sponsor-list')
    

class SponsorDetail(DetailView):
    model = Sponsor
    context_object_name = 'sponsor'
    
class SponsorList(ListView):
    model = Sponsor


# Project Views    
class ProjectCreate(CreateView):
    model = Project
    fields = ['title', 'acronym', 'researchers', 'git_repo', 'shared_drive']    
    
    def form_valid(self, form):
        self.object = form.save()        
        
        #Add Page to Notebook
        page = ProjectDashboardPage(title=form.cleaned_data['title'], intro="(place abstract here)", project_structure = self.object)      

        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        page.save_revision().publish()
        
        #Add in Default Page Sections
        print(self.model.default_sections)
        for section_name in self.model.default_sections:
            section_page = ProjectSectionPage(title=section_name, section_name=section_name)
            page.add_child(instance=section_page)
            section_page.save_revision().publish()

        return HttpResponseRedirect(page.url)


class ProjectUpdate(UpdateView):
    model = Project
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context 
    
    def form_valid(self, form):
        self.object = form.save()

        page = self.object.projectdashboardpage_set.first()
        page.title = form.cleaned_data['title']
        page.save_revision().publish()       
            
        return HttpResponseRedirect(page.url)
    

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
    fields = ['title', 'date', 'prepared_by', 'project_attendees']   
            
    def form_valid(self, form):
        projectId = self.kwargs['project']
        project = Project.objects.get(id=projectId)                
        
        self.object = form.save()
        self.object.project = project
        self.object.save()
        
        page = ProjectMeetingPage(title=self.object.title, meeting_structure = self.object)
        
        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        
        page.save_revision().publish() 

        return HttpResponseRedirect(page.url)


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
    

# Literature Views
class LiteratureCreate(CreateView):
    model = Literature
    fields = ['title']   
            
    def form_valid(self, form):
        projectId = self.kwargs['project']
        project = Project.objects.get(id=projectId)                
        
        self.object = form.save()
        self.object.project = project
        self.object.prepared_by.add(Researcher.objects.get(user=self.request.user))
        self.object.save()
        
        page = ProjectLiteraturePage(title=self.object.title, literature_structure=self.object)
        
        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        
        page.save_revision().publish() 

        return HttpResponseRedirect(page.url)


class LiteratureUpdate(UpdateView):
    model = Literature
    fields = '__all__'

class LiteratureDelete(DeleteView):
    model = Literature
    success_url = reverse_lazy('literature-list')
    
class LiteratureDetail(DetailView):
    model = Literature
    context_object_name = 'literature'
    
class LiteratureList(ListView):
    model = Literature
    
    
# Data Views
class DataCreate(CreateView):
    model = Data
    fields = ['title']   
            
    def form_valid(self, form):
        projectId = self.kwargs['project']
        project = Project.objects.get(id=projectId)                
        
        self.object = form.save()
        self.object.project = project
        self.object.prepared_by.add(Researcher.objects.get(user=self.request.user))
        self.object.save()
        
        page = ProjectDataPage(title=self.object.title, data_structure=self.object)
        
        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        
        page.save_revision().publish() 

        return HttpResponseRedirect(page.url)


class DataUpdate(UpdateView):
    model = Data
    fields = '__all__'

class DataDelete(DeleteView):
    model = Data
    success_url = reverse_lazy('data-list')
    
class DataDetail(DetailView):
    model = Data
    context_object_name = 'data'
    
class DataList(ListView):
    model = Data
    
    
# Analysis Views
class AnalysisCreate(CreateView):
    model = Analysis
    fields = ['title']   
            
    def form_valid(self, form):
        projectId = self.kwargs['project']
        project = Project.objects.get(id=projectId)                
        
        self.object = form.save()
        self.object.project = project
        self.object.prepared_by.add(Researcher.objects.get(user=self.request.user))
        self.object.save()
        
        page = ProjectAnalysisPage(title=self.object.title, analysis_structure=self.object)
        
        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        
        page.save_revision().publish() 

        return HttpResponseRedirect(page.url)


class AnalysisUpdate(UpdateView):
    model = Analysis
    fields = '__all__'

class AnalysisDelete(DeleteView):
    model = Analysis
    success_url = reverse_lazy('analysis-list')
    
class AnalysisDetail(DetailView):
    model = Analysis
    context_object_name = 'analysis'
    
class AnalysisList(ListView):
    model = Analysis
    
    
# Publication Views
class PublicationCreate(CreateView):
    model = Publication
    fields = ['title']   
            
    def form_valid(self, form):
        projectId = self.kwargs['project']
        project = Project.objects.get(id=projectId)                
        
        self.object = form.save()
        self.object.project = project
        self.object.prepared_by.add(Researcher.objects.get(user=self.request.user))
        self.object.save()
        
        page = ProjectPublicationPage(title=self.object.title, publication_structure=self.object)
        
        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        
        page.save_revision().publish() 

        return HttpResponseRedirect(page.url)


class PublicationUpdate(UpdateView):
    model = Publication
    fields = '__all__'

class PublicationDelete(DeleteView):
    model = Publication
    success_url = reverse_lazy('publication-list')
    
class PublicationDetail(DetailView):
    model = Publication
    context_object_name = 'publication'
    
class PublicationList(ListView):
    model = Publication
    
    
# Miscellaneous Views
class MiscCreate(CreateView):
    model = Misc
    fields = ['title']   
            
    def form_valid(self, form):
        projectId = self.kwargs['project']
        project = Project.objects.get(id=projectId)                
        
        self.object = form.save()
        self.object.project = project
        self.object.prepared_by.add(Researcher.objects.get(user=self.request.user))
        self.object.save()
        
        page = ProjectMiscPage(title=self.object.title, misc_structure=self.object)
        
        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        
        page.save_revision().publish() 

        return HttpResponseRedirect(page.url)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context['view'])
        section = ProjectSectionPage.objects.get(pk=context['view'].kwargs['pageId'])        
        
        context['section_name'] = section.section_name
        return context 


class MiscUpdate(UpdateView):
    model = Misc
    fields = '__all__'

class MiscDelete(DeleteView):
    model = Misc
    success_url = reverse_lazy('miscellaneous-list')
    
class MiscDetail(DetailView):
    model = Misc
    context_object_name = 'misc'
    
class MiscList(ListView):
    model = Misc
    

# Citation Edit Views
class CitationUpdate(UpdateView):
    model = Citation
    fields = '__all__'
    template_name_suffix = '_update_form'
    
    def form_valid(self, form):

        form.save()
        pageId = self.kwargs['pageId']
        page = Page.objects.get(id=pageId)
        
        return HttpResponseRedirect(page.url)
        
    
class CitationCreate(CreateView):
    model = Citation
    fields = '__all__'   
            
    def form_valid(self, form):
        projectId = self.kwargs['project']
        project = Project.objects.get(id=projectId)                
        
        self.object = form.save()
        self.object.project = project
        self.object.save()
        
        page = ProjectMiscPage(title=self.object.title, misc_structure=self.object)
        
        pageId = self.kwargs['pageId']       
        parent_page = Page.objects.get(id=pageId)
        parent_page.add_child(instance=page)
        
        page.save_revision().publish() 

        return HttpResponseRedirect(page.url)
