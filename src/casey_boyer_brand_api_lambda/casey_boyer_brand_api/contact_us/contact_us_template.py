import os
from casey_boyer_brand_api.aws.CustomerTableRecord import CustomerTableRecord
from jinja2 import Template


def build_message(record: CustomerTableRecord):
    template_file = os.path.join(os.path.dirname(__file__), "contact_us.html.j2")
    with open(template_file) as file_:
        template = Template(file_.read())

    return template.render(record=record)
