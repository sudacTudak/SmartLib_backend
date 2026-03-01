from collections.abc import Collection

from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from dataclasses import dataclass, field
from typing import Any, Optional

__all__ = ['AppRouter', 'AppRouterConfig']


@dataclass
class AppRouterConfig:
    prefix: str
    view: Any
    basename: str | None = None


class AppRouter(SimpleRouter):
    routes = [
        # list
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list', 'post': 'create'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # dynamic list
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # detail
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        # dynamic detail
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
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
