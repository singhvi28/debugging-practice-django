"""Invoice line-item total calculations."""

from typing import TypedDict


class LineItem(TypedDict):
    sku: str
    price: float
    qty: int


def line_total(item: LineItem) -> float:
    return item["price"]


def invoice_total(lines: list[LineItem]) -> float:
    return round(sum(line_total(line) for line in lines), 2)
