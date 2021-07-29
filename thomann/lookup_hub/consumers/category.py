import logging

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async as ds2a

from .base import HubConsumer
from ..models import Category, Dictionary
from ..serialisers import CategoryBarebonesSerialiser


LOGGER = logging.getLogger(__name__)


class CategoryConsumer(HubConsumer):
    async def connect(self):
        self.dictionary_name = self.scope["url_route"]["kwargs"]["dict_slug"]
        self.group_name = "_".join([self.dictionary_name, Category.GROUP_NAME])

        LOGGER.debug(f"Connecting to channel group {self.group_name}")

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()
        LOGGER.debug("Connected")

    async def receive_json(self, content, **kwargs):
        LOGGER.debug("CategoryConsumer receiving")
        LOGGER.debug(content)

        try:
            assert hasattr(self, content["method"])
            method = getattr(self, content["method"])
            LOGGER.debug(f"Method {content['method']} found")
            await method(content["data"])
        except AssertionError:
            LOGGER.warning(f"User tried to call method {content['method']}")
            await self.send_warning("Nice try.")
        except Exception as e:
            LOGGER.error(f"Exception in method {method}", exc_info=True)

    # async def create(self, event):
    #     LOGGER.debug("Creating")
    #     LOGGER.debug(event)
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             event["content"]
    #         }
    #     )

    async def read(self, cat_data):
        LOGGER.debug("Fetching category")

        category = await sync_to_async(Category.objects.get)(pk=cat_data["id"])
        cat_srl = CategoryBarebonesSerialiser(category)
        LOGGER.debug(cat_srl.data)

        await self.send_response("read", cat_srl.data)

    async def insert(self, cat_data):
        LOGGER.debug("Inserting category")

        prev_id = cat_data["id"]
        new_cat = await sync_to_async(self._insert_new_at)(obj_id=prev_id)
        cat_srl = CategoryBarebonesSerialiser(new_cat)

        response_data = {
            "prev_id": prev_id,
            "new_cat": cat_srl.data,
        }

        await self.send_response("inserted", response_data)

    # async def append(self, data):
    #     LOGGER.debug("Appending row")

    #     cat_id = data["id"]
    #     new_row = await sync_to_async(self._insert_new_at)(obj_id=cat_id, append=True)
    #     cat_srl = RowSerialiser(new_row)

    #     response_data = {
    #         "cat_id": cat_id,
    #         "new_row": cat_srl.data,
    #     }

    #     await self.send_response("appended", response_data)

    async def update(self, cat_data):
        LOGGER.debug("Updating category")
        LOGGER.debug(cat_data)

        try:
            cat = await sync_to_async(Category.objects.get)(pk=cat_data["id"])
            cat_srl = await sync_to_async(CategoryBarebonesSerialiser)(cat, data=cat_data, partial=True)

            if cat_srl.is_valid():
                await ds2a(cat_srl.save)()
                LOGGER.debug("Updated")
            else:
                LOGGER.warning("Cat data not valid")
                LOGGER.warning(cat_data)

        except Exception as e:
            LOGGER.error(e)
            return

        await self.send_response("updated", cat_srl.data)

    def _insert_new_at(self, obj_id):
        prev_cat = Category.objects.get(pk=obj_id)
        dictionary = Dictionary.objects.get(slug=self.dictionary_name)

        new_cat = Category(dictionary=dictionary)
        new_cat.save()
        LOGGER.debug("Created cat")

        new_cat.to(prev_cat.order + 1)
        LOGGER.debug("Moved cat")

        return new_cat
