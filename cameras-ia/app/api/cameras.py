from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.deps import get_manager, get_session_factory
from app.models import Camera
from app.schemas import CameraCreate, CameraOut, CameraUpdate

router = APIRouter(prefix="/api/cameras", tags=["cameras"])


def _get_or_404(session, camera_id: int) -> Camera:
    camera = session.get(Camera, camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Câmera não encontrada")
    return camera


def _to_out(camera: Camera, manager) -> CameraOut:
    out = CameraOut.model_validate(camera)
    out.online = manager.is_running(camera.id)
    return out


@router.get("", response_model=list[CameraOut])
def list_cameras(session_factory=Depends(get_session_factory), manager=Depends(get_manager)):
    with session_factory() as session:
        cameras = session.query(Camera).order_by(Camera.id).all()
        return [_to_out(c, manager) for c in cameras]


@router.post("", response_model=CameraOut, status_code=201)
def create_camera(
    payload: CameraCreate,
    session_factory=Depends(get_session_factory),
    manager=Depends(get_manager),
):
    with session_factory() as session:
        camera = Camera(**payload.model_dump())
        session.add(camera)
        session.commit()
        session.refresh(camera)
    if camera.enabled:
        manager.start_camera(camera.as_dict())
    return _to_out(camera, manager)


@router.get("/{camera_id}", response_model=CameraOut)
def get_camera(
    camera_id: int,
    session_factory=Depends(get_session_factory),
    manager=Depends(get_manager),
):
    with session_factory() as session:
        return _to_out(_get_or_404(session, camera_id), manager)


@router.patch("/{camera_id}", response_model=CameraOut)
def update_camera(
    camera_id: int,
    payload: CameraUpdate,
    session_factory=Depends(get_session_factory),
    manager=Depends(get_manager),
):
    with session_factory() as session:
        camera = _get_or_404(session, camera_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(camera, field, value)
        session.commit()
        session.refresh(camera)
    if camera.enabled:
        manager.start_camera(camera.as_dict())  # reinicia com a nova configuração
    else:
        manager.stop_camera(camera.id)
    return _to_out(camera, manager)


@router.delete("/{camera_id}", status_code=204)
def delete_camera(
    camera_id: int,
    session_factory=Depends(get_session_factory),
    manager=Depends(get_manager),
):
    manager.stop_camera(camera_id)
    with session_factory() as session:
        session.delete(_get_or_404(session, camera_id))
        session.commit()


@router.post("/{camera_id}/start", response_model=CameraOut)
def start_camera(
    camera_id: int,
    session_factory=Depends(get_session_factory),
    manager=Depends(get_manager),
):
    with session_factory() as session:
        camera = _get_or_404(session, camera_id)
        camera.enabled = True
        session.commit()
        session.refresh(camera)
    manager.start_camera(camera.as_dict())
    return _to_out(camera, manager)


@router.post("/{camera_id}/stop", response_model=CameraOut)
def stop_camera(
    camera_id: int,
    session_factory=Depends(get_session_factory),
    manager=Depends(get_manager),
):
    with session_factory() as session:
        camera = _get_or_404(session, camera_id)
        camera.enabled = False
        session.commit()
        session.refresh(camera)
    manager.stop_camera(camera_id)
    return _to_out(camera, manager)


@router.get("/{camera_id}/snapshot")
def snapshot(camera_id: int, manager=Depends(get_manager)):
    jpeg = manager.snapshot(camera_id)
    if jpeg is None:
        raise HTTPException(status_code=503, detail="Sem quadro disponível ainda")
    return Response(content=jpeg, media_type="image/jpeg")
