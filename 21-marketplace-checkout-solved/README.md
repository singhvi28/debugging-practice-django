# Marketplace Checkout (Django)

Practice debugging cart ownership, inventory reservation, coupons, idempotent checkout, and protected mutations.

Run `pip install -r requirements.txt && pytest -v`.

Routes: `GET /products`, `GET|POST /cart`, `POST /checkout`, `GET /orders/{id}`. Mutations require `Authorization: Bearer secret-token`; use `X-User` to select a cart and `Idempotency-Key` for checkout.
