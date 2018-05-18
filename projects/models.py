from django.db import models
from django.db.models import Max
from django.template.response import TemplateResponse

from wagtail.core.models import Page, PageQuerySet, PageManager
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from project_structure.models import Project, Researcher, Meeting, Literature, Data, Analysis, Publication, Misc

# Create your models here.

@register_snippet
class Sidebar(models.Model):
    pass

class ProjectsIndexPage(Page):
    intro = RichTextField(blank=True)

#    project_structure = models.ForeignKey(Project, on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]
    
    def updates(self):
        return ProjectNotePage.objects.all().order_by('-last_published_at')


class ProjectDashboardPage(RoutablePageMixin, Page):
    
    intro = RichTextField(blank=True)
    project_structure = models.ForeignKey(Project, on_delete=models.PROTECT)

    def get_notes(self):
        return ProjectNotePage.objects.live().descendant_of(self).specific().order_by('-last_published_at')

    def get_sections(self):
        return ProjectSectionPage.objects.live().descendant_of(self).specific().order_by('last_published_at')    
        
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('project_structure', classname="full"),
    ]
    
    @route(r'^addSection/$')
    def addSection(self, request):
        from .views import submit_sectionAdd
        return submit_sectionAdd(request, self)
        
    @route(r'^edit/(\w+)/$')
    @route(r'^edit/$')  
    def edit(self, request, fieldName=None):
        from .views import submit_dashboardEdit
        return submit_dashboardEdit(request, self, fieldName)


DEFAULT_SECTIONS = [
    'meeting',
    'literature',
    'data',
    'analysis',
    'publication',
]

class ProjectSectionPage(Page):

    section_name = models.CharField(max_length=100)    
    content_panels = Page.content_panels

    def project_structure(self):
        return ProjectDashboardPage.objects.ancestor_of(self).first().project_structure   

    def get_notes(self):
        return ProjectNotePage.objects.live().descendant_of(self).specific().order_by('-last_published_at')
        
    def add_note_url(self):
        if self.section_name.lower() not in DEFAULT_SECTIONS:
            return 'miscellaneous-add'
        return '{}-add'.format(self.section_name.lower())
    
    def __str__(self):
        return "{} Notes".format(self.section_name)
        
    @route(r'^addSection/$')
    def addSection(self, request):
        from .views import submit_sectionAdd
        return submit_sectionAdd(request, self)


class ProjectNotePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class ProjectMiscellaneousPage(ProjectNotePage):
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = ProjectNotePage.content_panels + [
        FieldPanel('author'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ] 

    
class ProjectMeetingPage(RoutablePageMixin, ProjectNotePage):            
    
    meeting_notes = RichTextField(blank=True)
    meeting_structure = models.ForeignKey(Meeting, on_delete=models.PROTECT)

    content_panels = ProjectNotePage.content_panels + [
        FieldPanel('meeting_structure', classname="full"),
    ]
    
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
          request,
          self.get_template(request),
          self.get_context(request)
        )

    @route(r'^edit/(\w+)/$')
    @route(r'^edit/$')  
    def edit(self, request, fieldName=None):
        from .views import submit_meetingEdit
        return submit_meetingEdit(request, self, fieldName)  


class ProjectLiteraturePage(RoutablePageMixin, ProjectNotePage):            
    
    literature_notes = RichTextField(blank=True)
    literature_structure = models.ForeignKey(Literature, on_delete=models.PROTECT)

    content_panels = ProjectNotePage.content_panels + [
        FieldPanel('literature_structure', classname="full"),
    ]
    
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
          request,
          self.get_template(request),
          self.get_context(request)
        )

    @route(r'^edit/(\w+)/$')
    @route(r'^edit/$')  
    def edit(self, request, fieldName=None):
        from .views import submit_literatureEdit
        return submit_literatureEdit(request, self, fieldName) 
        

class ProjectDataPage(RoutablePageMixin, ProjectNotePage):            
    
    data_notes = RichTextField(blank=True)
    data_structure = models.ForeignKey(Data, on_delete=models.PROTECT)

    content_panels = ProjectNotePage.content_panels + [
        FieldPanel('data_structure', classname="full"),
    ]
    
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
          request,
          self.get_template(request),
          self.get_context(request)
        )

    @route(r'^edit/(\w+)/$')
    @route(r'^edit/$')  
    def edit(self, request, fieldName=None):
        from .views import submit_dataEdit
        return submit_dataEdit(request, self, fieldName) 


class ProjectAnalysisPage(RoutablePageMixin, ProjectNotePage):            
    
    analysis_notes = RichTextField(blank=True)
    analysis_structure = models.ForeignKey(Analysis, on_delete=models.PROTECT)

    content_panels = ProjectNotePage.content_panels + [
        FieldPanel('analysis_structure', classname="full"),
    ]
    
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
          request,
          self.get_template(request),
          self.get_context(request)
        )

    @route(r'^edit/(\w+)/$')
    @route(r'^edit/$')  
    def edit(self, request, fieldName=None):
        from .views import submit_analysisEdit
        return submit_analysisEdit(request, self, fieldName) 
        

class ProjectPublicationPage(RoutablePageMixin, ProjectNotePage):            
    
    publication_notes = RichTextField(blank=True)
    publication_structure = models.ForeignKey(Publication, on_delete=models.PROTECT)

    content_panels = ProjectNotePage.content_panels + [
        FieldPanel('publication_structure', classname="full"),
    ]
    
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
          request,
          self.get_template(request),
          self.get_context(request)
        )

    @route(r'^edit/(\w+)/$')
    @route(r'^edit/$')  
    def edit(self, request, fieldName=None):
        from .views import submit_publicationEdit
        return submit_publicationEdit(request, self, fieldName)
        
        
class ProjectMiscPage(RoutablePageMixin, ProjectNotePage):            
    
    misc_notes = RichTextField(blank=True)
    misc_structure = models.ForeignKey(Misc, on_delete=models.PROTECT)

    content_panels = ProjectNotePage.content_panels + [
        FieldPanel('misc_structure', classname="full"),
    ]
    
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
          request,
          self.get_template(request),
          self.get_context(request)
        )

    @route(r'^edit/(\w+)/$')
    @route(r'^edit/$')  
    def edit(self, request, fieldName=None):
        from .views import submit_miscEdit
        return submit_miscEdit(request, self, fieldName)       
        

# DOMINGO: NOT ACTIVE vvv    
class ProjectUpdatesFeedPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]  

    
class ProjectCodeRepositoriesPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    
class ProjectPeoplePage(Page):
    intro = RichTextField(blank=True)

    project_structure = models.ForeignKey(Project, on_delete=models.PROTECT)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('project_structure', classname="full"),
    ]
