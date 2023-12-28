import os
from datetime import datetime
import cv2
import asyncio
import pyautogui
import websockets
from database.database_connection import DBManager
from utilities.config import WS_HOST, WS_PORT

db = DBManager()


async def configuration_websocket(websocket):
    # Gets the current event loop
    event_loop = asyncio.get_event_loop()

    # Creates two tasks 
    coordinate_task = event_loop.create_task(capturing_coordinates(websocket))
    click_task = event_loop.create_task(capture_clicks(websocket))

    # Waits until both tasks are completed
    await asyncio.wait([coordinate_task, click_task])


def get_cursor_position():
    coordinates = pyautogui.position()
    return coordinates[0], coordinates[1]


def capture_image(path: str, camera_port: int = 0):
    # Creates a VideoCapture object to connect to the camera
    camera = cv2.VideoCapture(camera_port)

    # Captures a single frame from the camera
    _, camera_capture = camera.read()

    # Saves the captured frame as an image file at a path
    cv2.imwrite(path, camera_capture)

    # Turns the captured frame in a PNG image and returns the binary representation of the image
    _, buffer = cv2.imencode(".png", camera_capture)

    return buffer


async def capturing_coordinates(websocket):
    # Infinitely sending mouse coordinates
    while True:
        coordinates = get_cursor_position()

        # Sending the coordinates as a string to the websocket
        await websocket.send(str(coordinates))


def coordinates_click(received_coordinates: str):
    # Location to save the images
    media_path = os.path.join(os.path.dirname(__file__), '../pictures')
    os.makedirs(media_path, exist_ok=True)

    # Create for image by clicking
    image = capture_image(os.path.join(media_path, f'{datetime.now()}.png'))

    # Inserts data in database
    db.insert_query(received_coordinates, image)


async def capture_clicks(websocket):
    # Receiving data from the websocket
    while True:
        data = await websocket.recv()
        coordinates_click(data)


async def start_websocket_server():
    db.setup()

    try:
        server = await websockets.serve(
            configuration_websocket, WS_HOST, WS_PORT,)

        print(f"The server started successfully: //{WS_HOST}:{WS_PORT}")
        await server.wait_closed()
    except Exception as err:
        print(f"Server failed to start: {err}")
