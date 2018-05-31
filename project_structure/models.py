from django.db import models
from django.urls import reverse
from django.forms import widgets
from django.utils.timezone import now

from django.conf import settings

from publications_bootstrap.models import Publication as BiBEntry

# Create your models here.

class Researcher(models.Model):
    first_name = models.CharField(max_length = 100)
    middle_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    website = models.URLField(blank=True)
    email = models.EmailField()
    degree = models.CharField(max_length = 100,
        choices = [
            ('Ph.D.', 'Ph.D.'),
            ('M.S.', 'M.S.'),
            ('M.A.', 'M.A.'),
            ('B.S.', 'B.S.'),
            ('B.A.', 'B.A.')
        ],    
    )
    active = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)    

    description = models.TextField(blank=True)    
    
    def get_absolute_url(self):
        return reverse('researcher-detail', kwargs={'pk': self.pk})
        
    def get_projects(self):
        Projects = self.project_set.all()
        pages = [project.projectdashboardpage_set.first() for project in Projects]
        return pages
        
    def short_name(self):
        return '{} {}'.format(first_name, last_name)
        
    def __str__(self):
        return '{} {}, {}'.format(self.first_name, self.last_name, self.degree)

    
class Sponsor(models.Model):
    first_name = models.CharField(max_length = 100)
    middle_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    title = models.CharField(max_length = 300, blank=True, verbose_name="Title in Organization")
    organization = models.CharField(max_length=300, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    org_description = models.TextField(blank=True, verbose_name="Organization Description")    
    
    def __str__(self):
        return '{} {}, {}'.format(self.first_name, self.last_name)
    

class Citation(BiBEntry):
    
    def long_cite(self):
        return "{}. {}, {}.".format(self.authors, self.title, self.year)
        
class Project(models.Model):
    title = models.CharField(max_length = 500)
    acronym = models.CharField(max_length = 10)
    description = models.TextField(default='', blank=True)
    researchers = models.ManyToManyField(Researcher)
    sponsors = models.ManyToManyField(Sponsor, blank=True)
    git_repo = models.URLField(blank=True)
    shared_drive = models.URLField(blank=True)
    citations = models.ManyToManyField(Citation, blank=True)

    default_sections = [
        'Meeting',
        'Literature',
        'Data',
        'Analysis',
        'Publication',
        'Miscellaneous',    
    ]

    def get_researchers(self):
        out = []
        for researcher in self.researchers.all():
            out += [researcher.id]
        return out
    
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return '{}: {}'.format(self.acronym, self.title)
        
        
class Meeting(models.Model):
    title = models.CharField(max_length=200)
    project_attendees = models.ManyToManyField(Researcher, related_name='project_attendees')
    prepared_by = models.ManyToManyField(Researcher, related_name='meeting_prepared_by')
    date = models.DateTimeField(default = now)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)

    def attendees(self):
        return self.project_attendees    
    
    def get_absolute_url(self):
        return reverse('meeting-detail', kwargs={'project': project.pk, 'pk': self.pk})
        

class Literature(models.Model):
    title = models.CharField(max_length=200)
    prepared_by = models.ManyToManyField(Researcher, related_name='literature_prepared_by')
    date = models.DateTimeField(default = now)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)
    citations = models.ManyToManyField(Citation, related_name='literature_citation')   
    
    def get_absolute_url(self):
        return reverse('literature-detail', kwargs={'project': project.pk, 'pk': self.pk})   
        

class Data(models.Model):
    title = models.CharField(max_length=200)
    prepared_by = models.ManyToManyField(Researcher, related_name='data_prepared_by')
    date = models.DateTimeField(default = now)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)    
    
    def get_absolute_url(self):
        return reverse('data-detail', kwargs={'project': project.pk, 'pk': self.pk})
        

class Analysis(models.Model):
    title = models.CharField(max_length=200)
    prepared_by = models.ManyToManyField(Researcher, related_name='analysis_prepared_by')
    date = models.DateTimeField(default = now)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)    
    
    def get_absolute_url(self):
        return reverse('analysis-detail', kwargs={'project': project.pk, 'pk': self.pk}) 
        

class Publication(models.Model):
    title = models.CharField(max_length=200)
    prepared_by = models.ManyToManyField(Researcher, related_name='publication_prepared_by')
    date = models.DateTimeField(default = now)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)    
    
    def get_absolute_url(self):
        return reverse('publication-detail', kwargs={'project': project.pk, 'pk': self.pk})
        

class Misc(models.Model):
    title = models.CharField(max_length=200)
    prepared_by = models.ManyToManyField(Researcher, related_name='misc_prepared_by')
    date = models.DateTimeField(default = now)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)    
    
    def get_absolute_url(self):
        return reverse('miscellaneous-detail', kwargs={'project': project.pk, 'pk': self.pk})       
        