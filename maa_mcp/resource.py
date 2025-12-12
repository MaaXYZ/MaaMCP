from typing import Optional

from maa.controller import Controller
from maa.resource import Resource
from maa.tasker import Tasker

from maa_mcp.core import object_registry
from maa_mcp.paths import get_resource_dir


# 全局资源 ID 的固定键名
_GLOBAL_RESOURCE_KEY = "_global_resource"


def get_or_create_resource() -> Optional[Resource]:
    """
    获取或创建全局唯一的 Resource 实例。
    注意：调用此函数前应确保 OCR 资源已存在，否则可能加载失败。
    """
    resource: Resource | None = object_registry.get(_GLOBAL_RESOURCE_KEY)
    if resource:
        return resource

    resource_path = get_resource_dir()

    resource = Resource()
    if not resource.post_bundle(str(resource_path)).wait().succeeded:
        return None

    object_registry.register_by_name(_GLOBAL_RESOURCE_KEY, resource)
    return resource


def get_or_create_tasker(controller_id: str) -> Optional[Tasker]:
    """
    根据 controller_id 获取或创建 tasker 实例。
    会自动加载全局资源。tasker 会被缓存，相同 controller 不会重复创建。
    """
    tasker_cache_key = f"_tasker_{controller_id}"
    tasker: Tasker | None = object_registry.get(tasker_cache_key)
    if tasker:
        return tasker

    controller: Controller | None = object_registry.get(controller_id)
    resource = get_or_create_resource()
    if not controller or not resource:
        return None

    tasker = Tasker()
    tasker.bind(resource, controller)
    if not tasker.inited:
        return None

    object_registry.register_by_name(tasker_cache_key, tasker)
    return tasker
