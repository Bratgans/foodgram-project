from recipes.models import Tag


def all_tags(request):
    """
        Вывод всех тегов.
    """
    all_tags = Tag.objects.all()
    return {'all_tags': all_tags}
