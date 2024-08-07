"""
Contains all the data structure for the different requests you can send to VTS
"""

from typing import Literal
from pydantic import BaseModel, ConfigDict


class BaseData(BaseModel):
    """
    Base for all Data Structures
    """

    model_config = ConfigDict(use_attribute_docstrings=True)


class BaseRequest(BaseModel):
    """
    The Base for all coming requests
    """

    apiName: str = "VTubeStudioPublicAPI"
    """Name of the API"""
    apiVersion: str = "1.0"
    """Version of the API"""
    requestID: str = "SomeID"
    """Id for the request, does not have to be unique"""
    messageType: str
    """Defining which request gets sent to VTubeStudio"""
    data: BaseData | None
    """The data associated with the request type, can be non in case messageType is """


class AuthenticationTokenRequestData(BaseData):
    """
    Data structure for an AuthenticationTokenRequest
    """

    pluginName: str = "PyVtsPlugin"
    """Name of the Plugin"""
    pluginDeveloper: str = "jaarfi"
    """Name of the Developer"""
    pluginIcon: str | None = None
    """optional: Base64 encoded PNG or JPG with exact dimensions of 128x128"""


class AuthenticationTokenRequest(BaseRequest):
    """
    Request an Authentication Token \n
    This will trigger a PopUp inside of VTubeStudio provided that Plugins are enabled
    """

    messageType: Literal["AuthenticationTokenRequest"] = "AuthenticationTokenRequest"
    data: AuthenticationTokenRequestData = AuthenticationTokenRequestData()
