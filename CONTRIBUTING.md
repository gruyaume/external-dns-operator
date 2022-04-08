# external-dns-operator

## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

## Testing

Tests are run with `tox`:

```bash
tox -e lint # Lint check
tox -e unit  # unit tests
tox -e static # static analysis
```
