# -*- coding: utf-8 -*-
import os
current_dir = os.path.dirname(os.path.realpath(__file__))


# REQUIRED: Which templates do you want to generate? (Use relative paths here!)
# Use strings (with single or double quotes), and separe each template in a line terminated with a comma. Such as examples below.
OUTPUT_TEMPLATES = [
    # 'some_template.jinja',
    # 'some_another_template.jinja',
]

# OPTIONAL: Where are the skeleton (.jinja) templates? - Defaults to 'jinja_templates' folder inside this project
INPUT_FOLDER = current_dir + '/jinja_templates'

# OPTIONAL: Which folder does it dump generated templates? - Defaults to 'html_templates' folder inside this project
OUTPUT_FOLDER = current_dir + '/html_templates'

# OPTIONAL: Do you have any additional variables to the templates? (use "'key': value" format)
EXTRA_VARIABLES = {
    # 'project_name': 'WaitCorp',
    # 'current_year': 2042,
    # 'debug': False,
}
