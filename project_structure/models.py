from django.db import models
from django.urls import reverse
from django.forms import widgets
from django.utils.timezone import now

# Create your models here.

class Researcher(models.Model):
    first_name = models.CharField(max_length = 100)
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
    
    def get_absolute_url(self):
        return reverse('researcher-detail', kwargs={'pk': self.pk})
        
    def short_name(self):
        return '{} {}'.format(first_name, last_name)
        
    def __str__(self):
        return '{} {}, {}'.format(self.first_name, self.last_name, self.degree)

        
class Project(models.Model):
    title = models.CharField(max_length = 500)
    acronym = models.CharField(max_length = 10)
    description = models.TextField(default='', blank=True)
    researchers = models.ManyToManyField(Researcher)
    git_repo = models.URLField(blank=True)
    shared_drive = models.URLField(blank=True)

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
    project_attendees = models.ManyToManyField(Researcher, related_name='project_attendees')
    prepared_by = models.ManyToManyField(Researcher, related_name='prepared_by')
    date = models.DateTimeField(default = now)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)

    def attendees(self):
        return self.project_attendees    
    
    def get_absolute_url(self):
        return reverse('meeting-detail', kwargs={'project': project.pk, 'pk': self.pk})
        
    
        
        
        