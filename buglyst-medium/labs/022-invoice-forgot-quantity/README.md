# The Invoice That Forgot Quantity

Carts with quantity greater than one are undercharged. Finance finds missing line totals.

## API

- `POST /invoice` — create an invoice with line items (`sku`, `price`, `qty`)

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
