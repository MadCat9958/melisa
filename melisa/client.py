from .models.app import Shard
from .utils.types import Coro

from .core.http import HTTPClient
from .core.gateway import GatewayBotInfo

import asyncio
from typing import Dict, List


class Client:
    def __init__(self, token, intents, **kwargs):
        self.shards: Dict[int, Shard] = {}
        self.http = HTTPClient(token)
        self._events = {}

        self.guilds = []

        self.loop = asyncio.get_event_loop()

        self._gateway_info = self.loop.run_until_complete(self._get_gateway())

        self.intents = intents
        self._token = token

        self._activity = kwargs.get("activity")
        self._status = kwargs.get("status")

    async def _get_gateway(self):
        """Get Gateway information"""
        return GatewayBotInfo.from_dict(await self.http.get("gateway/bot"))

    def listen(self, callback: Coro):
        """Method to set the listener.

        Parameters
        ----------
        callback (:obj:`function`)
            Coroutine Callback Function
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError(f"<{callback.__qualname__}> must be a coroutine function")

        self._events[callback.__qualname__] = callback
        return self

    def run(self) -> None:
        """
            Run Bot without shards (only 0 shard)
        """
        inited_shard = Shard(self, 0, 1)

        asyncio.ensure_future(inited_shard.launch(activity=self._activity, status=self._status), loop=self.loop)
        self.loop.run_forever()

    def run_shards(self, num_shards: int, *, shard_ids: List[int] = None):
        """
            Run Bot with shards specified by the user.

            Parameters
            ----------
            num_shards : :class:`int`
                The endpoint to send the request to.

            Keyword Arguments:

            shard_ids: Optional[:class:`List[int]`]
                List of Ids of shards to start.
        """
        if not shard_ids:
            shard_ids = range(num_shards)

        for shard_id in shard_ids:
            inited_shard = Shard(self, shard_id, num_shards)

            asyncio.ensure_future(inited_shard.launch(activity=self._activity, status=self._status), loop=self.loop)
        self.loop.run_forever()

    def run_autosharded(self):
        """
            Runs the bot with the amount of shards specified by the Discord gateway.
        """
        num_shards = self._gateway_info.shards
        shard_ids = range(num_shards)

        for shard_id in shard_ids:
            inited_shard = Shard(self, shard_id, num_shards)

            asyncio.ensure_future(inited_shard.launch(activity=self._activity, status=self._status), loop=self.loop)
        self.loop.run_forever()

