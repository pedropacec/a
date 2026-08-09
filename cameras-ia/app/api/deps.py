from __future__ import annotations

from fastapi import Request

from app.core.manager import CameraManager


def get_session_factory(request: Request):
    return request.app.state.session_factory


def get_manager(request: Request) -> CameraManager:
    return request.app.state.manager
