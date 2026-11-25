"""Response body decoding based on Content-Type."""


def decode_body(content: bytes, content_type: str) -> str:
    charset = "utf-8"
    if "charset=" in content_type.lower():
        charset = content_type.split("charset=")[-1].split(";")[0].strip()

    return content.decode("utf-8")
