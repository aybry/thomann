import logging

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async as ds2a

from .base import HubConsumer
from ..models import Row, Category
from ..serialisers import RowSerialiser


LOGGER = logging.getLogger(__name__)
CHANNEL_NAME = "hub"


class RowConsumer(HubConsumer):
    async def connect(self):
        dictionary_name = self.scope["url_route"]["kwargs"]["dict_slug"]
        self.group_name = "_".join([dictionary_name, Row.GROUP_NAME])

        LOGGER.debug(f"Connecting to channel group {self.group_name}")

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()
        LOGGER.debug("Connected")

    async def receive_json(self, content, **kwargs):
        LOGGER.debug("RowConsumer receiving")
        LOGGER.debug(content)

        try:
            assert hasattr(self, content["method"])
            method = getattr(self, content["method"])
            LOGGER.debug(f"Method {content['method']} found")
            await method(content["data"])
        except AssertionError:
            LOGGER.warning(f"User tried to call method {content['method']}")
            await self.send_warning("Nice try.")
        except Exception:
            LOGGER.error(f"Exception in method {method}", exc_info=True)

    async def read(self, row_data):
        LOGGER.debug("Fetching row")

        row = await sync_to_async(Row.objects.get)(pk=row_data["id"])
        row_srl = RowSerialiser(row)
        LOGGER.debug(row_srl.data)

        await self.send_response("read", row_srl.data, to_group=False)

    async def insert(self, row_data):
        LOGGER.debug("Inserting row")

        prev_id = row_data["id"]
        new_row = await sync_to_async(self._insert_new_at)(obj_id=prev_id)
        row_srl = RowSerialiser(new_row)

        response_data = {
            "prev_id": prev_id,
            "new_row": row_srl.data,
        }

        await self.send_response("inserted", response_data)


    async def append(self, data):
        LOGGER.debug("Appending row")

        cat_id = data["id"]
        new_row = await sync_to_async(self._insert_new_at)(obj_id=cat_id, append=True)
        row_srl = RowSerialiser(new_row)

        response_data = {
            "cat_id": cat_id,
            "new_row": row_srl.data,
        }

        await self.send_response("appended", response_data)

    async def update(self, row_data):
        LOGGER.debug("Updating row")
        LOGGER.debug(row_data)

        try:
            row = await sync_to_async(Row.objects.get)(pk=row_data["id"])
            row_srl = await sync_to_async(RowSerialiser)(row, data=row_data, partial=True)

            if row_srl.is_valid():
                await ds2a(row_srl.save)()
                LOGGER.debug("Updated")
            else:
                LOGGER.warning("Row data not valid")
                LOGGER.warning(row_data)

        except Exception as e:
            LOGGER.error(e)
            return

        await self.send_response("updated", row_srl.data)

    async def delete(self, row_data):
        LOGGER.debug("Deleting row")
        row_id = row_data["id"]

        row = await sync_to_async(Row.objects.get)(pk=row_id)
        await sync_to_async(row.delete)()

        await self.send_response("deleted", {"id": row_id})

    def _insert_new_at(self, obj_id, append=False):
        if append:
            category = Category.objects.get(pk=obj_id)
        else:
            row = Row.objects.get(pk=obj_id)
            category = row.category

        new_row = Row(category=category)
        new_row.save()
        LOGGER.debug("Created row")

        if not append:
            new_row.to(row.order)
            LOGGER.debug("Moved row")

        return new_row
