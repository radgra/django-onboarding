from django import template

register = template.Library()

@register.simple_tag
def class_for_state(onboarding_task):
    if onboarding_task.state == 'CM':
        return 'teal white-text'
    if onboarding_task.state == 'PR':
        return 'orange'
    if onboarding_task.state == 'NC':
        return 'red white-text'
    
    return None