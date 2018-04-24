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
from project_structure.models import Project, Researcher, Meeting

# Create your models here.

@register_snippet
class Sidebar(models.Model):
    pass

class ProjectsIndexPage(Page):
    intro = RichTextField(blank=True)

    project_structure = models.ForeignKey(Project, on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('project_structure', classname="full"),
    ]
    
    def updates(self):
        return Page.objects.all().order_by('-last_published_at')

class ProjectPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class ProjectBlankPage(Page):
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ] 
    
    
class ProjectDashboardPage(Page):
    intro = RichTextField(blank=True)

    project_structure = models.ForeignKey(Project, on_delete=models.PROTECT)

    def get_meetings(self):
        return ProjectMeetingPage.objects.live().descendant_of(self).specific().order_by('-last_published_at')

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('project_structure', classname="full"),
    ]
    
class ProjectPeoplePage(Page):
    intro = RichTextField(blank=True)

    project_structure = models.ForeignKey(Project, on_delete=models.PROTECT)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('project_structure', classname="full"),
    ]

    
class ProjectMeetingPage(RoutablePageMixin, Page):            
    
    intro = RichTextField(blank=True)
    meeting_notes = RichTextField(blank=True)
    meeting_structure = models.ForeignKey(Meeting, on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
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
    
