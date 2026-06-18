from django import template
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

register = template.Library()


@register.filter
def markdownify(text):
    return markdown(
    text,
    extensions=[
        "fenced_code",
        "tables",
        CodeHiliteExtension(css_class="highlight"),
    ]
)