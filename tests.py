import os
import tempfile
from prompter.prompt_template_processor import PromptTemplateProcessor

def test_basic_variable():
    with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
        tf.write('Hello, {{name}}!')
        tf.flush()
        processor = PromptTemplateProcessor(tf.name)
        result = processor.render({'name': 'World'})
        assert result == 'Hello, World!'
    os.unlink(tf.name)

def test_function_no_params():
    with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
        tf.write('Greeting: {{greet}}')
        tf.flush()
        processor = PromptTemplateProcessor(tf.name)
        result = processor.render({'greet': lambda: 'Hi there'})
        assert result == 'Greeting: Hi there'
    os.unlink(tf.name)

def test_function_with_params():
    with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
        tf.write('Sum: {{add}}')
        tf.flush()
        processor = PromptTemplateProcessor(tf.name)
        def add(a, b):
            return str(a + b)
        result = processor.render({'add': add, 'a': 2, 'b': 3})
        assert result == 'Sum: 5'
    os.unlink(tf.name)

def test_missing_param():
    with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
        tf.write('Sum: {{add}}')
        tf.flush()
        processor = PromptTemplateProcessor(tf.name)
        def add(a, b):
            return str(a + b)
        try:
            processor.render({'add': add, 'a': 2})
        except ValueError as e:
            assert 'Missing required parameters' in str(e)
        else:
            assert False, 'Expected ValueError for missing parameter'
    os.unlink(tf.name)

if __name__ == '__main__':
    test_basic_variable()
    test_function_no_params()
    test_function_with_params()
    test_missing_param()
    print('All tests passed!')

