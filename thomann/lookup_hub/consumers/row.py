import logging
from datetime import datetime

from asgiref.sync import sync_to_async
# from channels.db import database_sync_to_async as ds2a

from .base import HubConsumer
from ..models import Row, Category
from ..serialisers import RowSerialiser, DeletedRowSerialiser


LOGGER = logging.getLogger(__name__)
CHANNEL_NAME = "hub"


class RowConsumer(HubConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            self.accept()
            self.send_warning("You are not authenticated!")
            self.disconnect()

        self.dictionary_name = self.scope["url_route"]["kwargs"]["dict_slug"]
        self.group_name = "_".join([self.dictionary_name, Row.GROUP_NAME])

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
            await method(content.get("data"))
        except AssertionError:
            LOGGER.warning(f"User tried to call method {content['method']}")
            await self.send_warning("Nice try.")
        except Exception:
            LOGGER.error(f"Exception in method {method}", exc_info=True)

    async def read(self, row_data):
        LOGGER.debug("Fetching row")

        row = await sync_to_async(Row.objects.get)(pk=row_data["id"])
        row_srl = RowSerialiser(row)
        row_srl_data = await sync_to_async(getattr)(row_srl, "data")
        LOGGER.debug(row_srl_data)

        await self.send_response("read", row_srl_data, to_group=False)

    async def read_deleted(self, *_):
        LOGGER.debug("Fetching deleted rows")

        deleted_rows = Row.objects.filter(**{
            "deleted_from__dictionary__slug": self.dictionary_name,
            "is_deleted": True,
        }).order_by("-deleted_at")[:10]

        row_srl = DeletedRowSerialiser(deleted_rows, many=True)
        row_srl_data = await sync_to_async(getattr)(row_srl, "data")
        LOGGER.debug(row_srl_data)

        await self.send_response("read_deleted", row_srl_data, to_group=False)

    async def insert(self, row_data):
        LOGGER.debug("Inserting row")

        prev_id = row_data["id"]
        new_row = await sync_to_async(self._insert_new_at)(obj_id=prev_id)
        row_srl = RowSerialiser(new_row)
        row_srl_data = await sync_to_async(getattr)(row_srl, "data")

        response_data = {
            "prev_id": prev_id,
            "new_row": row_srl_data,
        }

        await self.send_response("inserted", response_data)


    async def append(self, data):
        LOGGER.debug("Appending row")

        cat_id = data["id"]
        new_row = await sync_to_async(self._insert_new_at)(obj_id=cat_id, append=True)
        row_srl = RowSerialiser(new_row)
        row_srl_data = await sync_to_async(getattr)(row_srl, "data")

        response_data = {
            "cat_id": cat_id,
            "new_row": row_srl_data,
        }

        await self.send_response("appended", response_data)

    async def update(self, row_data):
        LOGGER.debug("Updating row")
        LOGGER.debug(row_data)

        try:
            row_srl = await sync_to_async(self._update_row)(new_row_data=row_data)
        except Exception as e:
            LOGGER.error(e)
            await self.send_warning("Row update failed")
            return

        row_srl_data = await sync_to_async(getattr)(row_srl, "data")

        await self.send_response("updated", row_srl_data)

    async def delete(self, row_data):
        LOGGER.debug("Deleting row")
        row_id = row_data["id"]

        try:
            await sync_to_async(self._delete_row)(row_id)
        except Exception as e:
            LOGGER.error(e)
            await self.send_warning("Row update failed")

            return

        await self.send_response("deleted", {"id": row_id})

    async def restore(self, row_data):
        LOGGER.debug("Restoring row")
        row_id = row_data["id"]

        try:
            row_srl, prev_id = await sync_to_async(self._restore_row)(row_id)
        except Exception as e:
            LOGGER.error(e)
            await self.send_warning("Row restore failed")
            return

        row_srl_data = await sync_to_async(getattr)(row_srl, "data")

        if prev_id is None:
            response_data = {
                "cat_id": row_srl_data["category"],
                "new_row": row_srl_data,
                "subaction": "restored",
            }
            await self.send_response("appended", response_data)

        else:
            response_data = {
                "prev_id": prev_id,
                "new_row": row_srl_data,
                "subaction": "restored",
            }
            await self.send_response("inserted", response_data)

    def _update_row(self, *, new_row_data):
        row = Row.objects.get(pk=new_row_data["id"])
        row_srl = RowSerialiser(row, data=new_row_data, partial=True)

        if row_srl.is_valid():
            row_srl.save()
            LOGGER.debug("Updated")
        else:
            LOGGER.warning("Row update data not valid")
            LOGGER.warning(new_row_data)

        return row_srl

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

    def _delete_row(self, row_id):
        row = Row.objects.get(pk=row_id)

        new_row_data = {
            "id": row_id,
            "category": None,
            "deleted_from": row.category.id,
            "is_deleted": True,
            "deleted_at": datetime.now(),
        }

        row_srl = RowSerialiser(row, data=new_row_data, partial=True)

        if row_srl.is_valid():
            LOGGER.info(row_srl.validated_data)
            row_srl.save()
            LOGGER.debug("Deleted")

        else:
            LOGGER.warning("Row delete data not valid")
            LOGGER.warning(row_srl.errors)
            LOGGER.warning(row_srl.data)

    def _restore_row(self, row_id):
        row = Row.objects.get(pk=row_id)
        next_row = Row.objects.filter(
            category=row.deleted_from,
            order__gt=row.order,
        ).first()

        new_row_data = {
            "category": row.deleted_from.id,
            "deleted_from": None,
            "is_deleted": False,
            "deleted_at": None,
        }

        row_srl = RowSerialiser(row, data=new_row_data, partial=True)

        if row_srl.is_valid():
            LOGGER.info(row_srl.validated_data)
            row_srl.save()
            LOGGER.debug("Restored")
        else:
            LOGGER.warning("Row restore data not valid")
            LOGGER.warning(row_srl.errors)
            LOGGER.warning(row_srl.data)

        return row_srl, getattr(next_row, "id", None)
