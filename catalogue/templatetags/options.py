
from django import template

from catalogue.models import Option


class GetOption(template.Node):
    def __init__(self, name, var_name) -> None:
        self.name = name
        self.var_name = var_name
        super().__init__()
    def render(self, context) -> str:
        opt = None
        print('*'*10)
        print(self.var_name, self.name)
        try:
            opt = Option.objects.get(name=self.name)
        except:
            print('not found.....')
        context[self.var_name] = opt
        return ''



register = template.Library()

@register.tag(name='get_option')
def get_option(parser, token):
    error = False
    try:
        tag_name, name, _as, var_name = token.split_contents()
        if _as != 'as':
            error = True
    except:
        error = True
    
    if error:
        pass
    else:
        return GetOption(name, var_name)

@register.simple_tag
def compute_price(product ,collection=None):
    return int(product.compute_price(collection))