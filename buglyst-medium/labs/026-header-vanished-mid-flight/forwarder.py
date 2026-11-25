"""Outbound request forwarding to an internal echo service."""

from collections.abc import Callable

EchoHandler = Callable[[dict[str, str]], dict]


def forward(headers: dict[str, str], echo_handler: EchoHandler) -> dict:
    outbound = {k: v for k, v in headers.items() if k.lower() != "authorization"}
    return echo_handler(outbound)
