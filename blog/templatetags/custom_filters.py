from django import template

register = template.Library()

@register.filter(name='user_can_modify')
def user_can_modify(post, user):
    if post is None:
        return False
    return post.user_can_modify(user)
