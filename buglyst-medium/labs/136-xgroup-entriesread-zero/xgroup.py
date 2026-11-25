"""Redis-style XGROUP argument builder."""


def build_xgroup_args(
    command: str,
    stream: str,
    group: str,
    stream_id: str,
    *,
    entries_read: int | None = None,
    mkstream: bool = False,
) -> list[str]:
    args: list[str] = ["XGROUP", command, stream, group, stream_id]
    if mkstream:
        args.append("MKSTREAM")
    if entries_read:
        args.extend(["ENTRIESREAD", str(entries_read)])
    return args
