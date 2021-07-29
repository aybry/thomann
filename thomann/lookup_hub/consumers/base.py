import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer


LOGGER = logging.getLogger(__name__)


class HubConsumer(AsyncJsonWebsocketConsumer):
    async def send_warning(self, message):
        LOGGER.debug(f"Sending warning: '{message}'")
        await self.send_json({
            "action": "warning",
            "message": message,
        })

    async def send_response(self, action, data, to_group=True):
        if to_group:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "send_json",
                    "action": action,
                    "data": data,
                }
            )
        else:
            await self.send_json({
                "action": action,
                "data": data,
            })