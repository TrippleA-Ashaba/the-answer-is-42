from django.views.generic import TemplateView

from .utils import BlogAPI


class BlogIndexView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = BlogAPI().get_posts()
        if not isinstance(posts, list):
            context["error"] = posts
            context["posts"] = []
        else:
            context["posts"] = posts
        return context
