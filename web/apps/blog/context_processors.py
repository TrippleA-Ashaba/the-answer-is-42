from django.utils import timezone


def current_year(request):
    """This context processor will add the current year to the context of every template in the project."""
    return {"current_year": timezone.now().year}
