from collections.abc import Collection

from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from dataclasses import dataclass
from typing import Any, Optional

__all__ = ['AppRouter', 'AppRouterConfig']


@dataclass
class AppRouterConfig:
    prefix: str
    view: Any
    basename: Optional[str]


class AppRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list', 'post': 'create'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]

    @classmethod
    def from_configs(cls, configs: Collection[AppRouterConfig], /, **kwargs):
        instance = cls(**kwargs)

        for config in configs:
            instance.register(config.prefix, config.view, basename=config.basename)

        return instance
