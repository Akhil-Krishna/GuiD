from django import template

register = template.Library()

@register.filter
def format_hms(td):
    total_seconds = int(td.total_seconds())
    hours = (total_seconds // 3600) % 24
    minutes = (total_seconds // 60) % 60
    seconds = total_seconds % 60
    
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
