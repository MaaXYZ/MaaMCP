import json
import webbrowser

from lzstring import LZString

from maa_mcp.core import mcp

# MPE 分享协议版本
SHARE_VERSION = 1
# URL 参数名
SHARE_PARAM = "shared"
# 默认 MPE 基准地址
DEFAULT_MPE_BASE_URL = "https://mpe.codax.site/stable"


def generate_share_link(
    pipeline_obj: dict, base_url: str = DEFAULT_MPE_BASE_URL
) -> str:
    # 生成分享链接
    payload = {
        "v": SHARE_VERSION,
        "d": pipeline_obj,
    }
    json_string = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    lz = LZString()
    compressed = lz.compressToEncodedURIComponent(json_string)
    share_url = f"{base_url}?{SHARE_PARAM}={compressed}"
    return share_url


@mcp.tool(
    name="open_pipeline_in_mpe",
    description="""
    将 Pipeline JSON 生成 MPE（MaaPipelineEditor）可视化链接并在浏览器中打开。

    参数：
    - pipeline_json: Pipeline 的 JSON 字符串或 dict 对象
    - base_url: MPE 基准地址（可选），默认为 "https://mpe.codax.site/stable"

    功能说明：
    该工具会将传入的 Pipeline 数据压缩编码后生成一个分享链接，
    并自动在系统默认浏览器中打开，方便用户可视化查看工作流结构。

    注意：
    - 此工具无返回值，仅执行打开浏览器的操作
    - 仅在用户明确要求预览可视化 Pipeline 工作流时生成并打开分享链接
    """,
)
def open_pipeline_in_mpe(
    pipeline_json: dict | str,
    base_url: str = DEFAULT_MPE_BASE_URL,
) -> None:
    # 如果传入的是字符串，先解析为 dict
    if isinstance(pipeline_json, str):
        pipeline_obj = json.loads(pipeline_json)
    else:
        pipeline_obj = pipeline_json

    # 生成分享链接
    share_url = generate_share_link(pipeline_obj, base_url)

    # 在浏览器中打开
    webbrowser.open(share_url)
