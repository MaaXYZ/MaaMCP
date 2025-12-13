import time
from datetime import datetime

from maa_mcp.core import mcp


@mcp.tool(
    name="wait",
    description="""
    等待指定的时间（秒）。
    当需要等待界面加载、动画完成或操作生效时，以及其他需要等待的情况下使用。
    注意：由于客户端超时限制，单次等待最长支持 60 秒。如果需要等待更长时间，请多次调用。
    """,
)
def wait(seconds: float) -> str:
    MAX_WAIT = 60.0
    if seconds > MAX_WAIT:
        time.sleep(MAX_WAIT)
        return f"已等待 {MAX_WAIT} 秒（单次最大限制）。请再次调用 wait 以继续等待剩余时间。"

    time.sleep(seconds)
    return f"已等待 {seconds} 秒"


@mcp.tool(
    name="get_current_datetime",
    description="""
    获取当前时间字符串（年月日时分秒），用于在需要时间信息时避免猜测。

    返回值示例：
    - 2025-12-14 10:23:45
    """,
)
def get_current_datetime() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
