"""Payment gateway client."""

from dataclasses import dataclass


@dataclass
class PaymentRequest:
    amount_cents: int
    authorization: str


class PaymentError(Exception):
    def __init__(self, request: PaymentRequest):
        self.request = request
        super().__init__(f"payment failed for request {request}")


def charge(request: PaymentRequest) -> dict:
    if not request.authorization.startswith("sk_live_"):
        raise PaymentError(request)
    if request.amount_cents <= 0:
        raise PaymentError(request)
    return {"status": "captured", "amount_cents": request.amount_cents}
