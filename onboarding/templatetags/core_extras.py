from django import template

register = template.Library()

@register.simple_tag
def class_for_state(onboarding_task):
    if onboarding_task.state == 'CM':
        return 'green darken-2 white-text'
    if onboarding_task.state == 'PR':
        return 'orange darken-2 white-text'
    if onboarding_task.state == 'NC':
        return 'red white-text'
    if onboarding_task.state == 'ST':
        return 'blue darken-2 white-text'
    
    return None