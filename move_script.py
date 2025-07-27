import os
import shutil

src = os.path.join(os.path.dirname(__file__), '..', 'prompt_template_processor.py')
dst = os.path.join(os.path.dirname(__file__), 'prompter', 'prompt_template_processor.py')
shutil.move(src, dst)

