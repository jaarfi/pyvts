import websockets
import asyncio
import requests_vts
import vts
import json

myvts = vts.Vts()
asyncio.run(myvts.connect())
request = requests_vts.AuthenticationTokenRequest()
dumpy = request.model_dump_json()
response = asyncio.run(myvts.request(requests_vts.AuthenticationTokenRequest()))
print(response)

# myvts = vts.vts()
# response = myvts.request(requests_vts.AuthenticationTokenRequest().model_dump())
# print(response)
