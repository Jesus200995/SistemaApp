from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from fastapi.websockets import WebSocketState

router = APIRouter(prefix="/chat", tags=["Chat en tiempo real"])

active_connections: List[WebSocket] = []


async def connect_user(websocket: WebSocket):
    """Conectar un cliente WebSocket al chat"""
    await websocket.accept()
    active_connections.append(websocket)


async def disconnect_user(websocket: WebSocket):
    """Desconectar un cliente del chat"""
    if websocket in active_connections:
        active_connections.remove(websocket)


async def broadcast_message(message: str):
    """Enviar mensaje a todos los clientes conectados"""
    for connection in active_connections:
        if connection.application_state == WebSocketState.CONNECTED:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"❌ Error broadcasting: {e}")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para chat en tiempo real"""
    await connect_user(websocket)
    print(f"✅ Cliente conectado. Total: {len(active_connections)}")
    
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast_message(data)
    except WebSocketDisconnect:
        await disconnect_user(websocket)
        print(f"🔴 Cliente desconectado. Total: {len(active_connections)}")
    except Exception as e:
        print(f"❌ Error en WebSocket: {e}")
        await disconnect_user(websocket)


@router.get("/status")
async def chat_status():
    """Obtener estado del chat"""
    return {
        "connected_users": len(active_connections),
        "status": "✅ Chat funcionando correctamente"
    }
