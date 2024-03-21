
from robyn import Robyn
import django
from django.conf import settings
from django.views import generic
import os
import sys
from robyn.templating import JinjaTemplate
from django.utils.crypto import get_random_string
from time import time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
django.setup()

app = Robyn(__file__)

old_nested = sys.modules['robyn'].get_all_nested

def return_functions(view, *args, **kwargs):
    if issubclass(view, generic.base.View):
        return [(method, view.as_view())for method in view.http_method_names]
    return old_nested(view, *args, **kwargs)

sys.modules['robyn'].get_all_nested = return_functions



@app.view("/")
class RustTemplateView(generic.TemplateView):
    template_name = "index.html"
    response_class = JinjaTemplate(settings.BASE_DIR / "templates")

    def render_to_response(self, context, **kwargs):
        start = time()
        for _ in range(10000):
            context['something'] = self.response_class.env.get_template('something.html').render(somebody=f"it's me, {get_random_string(10)}")
        print(time() - start)
        return self.response_class.render_template(template_name=self.template_name, **context)


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8000)
