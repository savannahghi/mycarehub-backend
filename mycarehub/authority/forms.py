from mycarehub.authority.models import AuthorityRole


def get_role_choices():
    choices = []
    for role in AuthorityRole.objects.all():
        choices.append((role.name, role.name))

    return choices
