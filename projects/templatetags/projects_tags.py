from django import template
from ..models import ProjectDashboardPage

register = template.Library()

@register.inclusion_tag('projects/tags/sidebar.html', takes_context=True)
def sidebar(context):
    return {
        'projects': ProjectDashboardPage.objects.order_by('title').all(),
        'request': context['request'],
    }
