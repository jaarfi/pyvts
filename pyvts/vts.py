""" main class """

import json
import websockets
import aiofiles
import config
import error
import base64
import cv2
import os
import requests_vts


class vts:
    """
    ``VtubeStudio API`` Connector

    Args
    ----------
    plugin_info : dict of {"plugin_name", "developer", "plugin_icon", "authentication_token_path"}

        Information about your plugin.

    vts_api_info: dict of {"version", "name", "port"}
        Information about VTubeStudio API.

    **kwarg :
        In case you just want to change serveral of the plugin/api Args,
        input your data here

    Examples
    --------
    Using ``Args``

    >>> info = {"plugin_name": "a","developer": "b",
    ...         "authentication_token_path": "./token.txt"}
    >>> pyvts.vts(plugin_info=info)

    Using ``**kwarg``

    >>> pyvts.vts(plugin_name="a", developer="b")

    """

    def __init__(
        self,
        plugin_info: dict = config.plugin_default,
        vts_api_info: dict = config.vts_api,
        **kwargs
    ) -> None:
        if "host" in vts_api_info:
            self.host = vts_api_info["host"]
        else:
            self.host = "localhost"
        self.port = vts_api_info["port"]
        self.websocket = None
        self.authentic_token = None
        self.__connection_status = 0  # 0: not connected, 1: connected
        self.__authentic_status = (
            0  # 0:no authen & token, 1:has token, 2:authen, -1:wrong token
        )
        self.api_name = vts_api_info["name"]
        self.api_version = vts_api_info["version"]
        self.plugin_name = plugin_info["plugin_name"]
        self.plugin_developer = plugin_info["developer"]
        self.plugin_icon = (
            plugin_info["plugin_icon"] if "plugin_icon" in plugin_info.keys() else None
        )
        self.icon = None
        self.token_path = plugin_info["authentication_token_path"]
        self.event_list = []
        self.recv_histroy = []
        for key, value in kwargs.items():
            setattr(self, key, value)

    async def connect(self) -> None:
        """Connect to VtubeStudio API server"""
        try:
            self.websocket = await websockets.connect("ws://localhost:8001")
            self.__connection_status = 1
            print("Succesfully connected")
        except error.ConnectionError as e:
            print("Error: ", e)
            print("Please ensure VTubeStudio is running and")
            print("the API is running on ws://localhost:", str(self.port))

    async def close(self) -> None:
        """
        Close connection
        """
        await self.websocket.close(code=1000, reason="user closed")
        self.__connection_status = 0

    async def request(self, request_msg: requests_vts.BaseRequest) -> dict:
        """
        Send request to VTubeStudio

        Args
        ----------
        request_msg : dict
            Message generated from `VTSRequest`

        Returns
        -------
        response_dict
            Message from VTubeStudio API, data is stored in ``return_dict["data"]``

        Examples
        --------
        >>> recv_msg = await myvts.request(send_msg)
        >>> recv_data = recv_msg["data"]
        """
        dumpy = request_msg.model_dump_json()
        print(dumpy)
        await self.websocket.send(dumpy)
        response_msg = await self.websocket.recv()
        response_dict = json.loads(response_msg)
        return response_dict
