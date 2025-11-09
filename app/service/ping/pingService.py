from app.repository.ping.pingCheck import ping_check


def ping_service() -> dict[str, str]:
    return ping_check()
 