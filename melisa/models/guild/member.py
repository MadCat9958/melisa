# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from melisa.utils.timestamp import Timestamp
from melisa.utils.snowflake import Snowflake
from melisa.models.user.user import User
from melisa.utils.types import APINullable
from melisa.utils.api_model import APIModelBase


@dataclass(repr=False)
class GuildMember(APIModelBase):
    """
    This model represents a guild member.

    **The field user won't be included in the member object
    attached to ``MESSAGE_CREATE`` and ``MESSAGE_UPDATE`` gateway events.**

    In ``GUILD_`` events, ``pending`` will always be included as true or false.
    In non ``GUILD_`` events which can only be triggered by non-``pending`` users, ``pending`` will not be included.

    Attributes
    -----------
    user: :class:`~melisa.models.user.user.User`
        The user this guild member represents
    nick: Optional[:class:`str`]
        This user's guild nickname
    avatar: Optional[:class:`str`]
        The member's guild avatar hash
    role_ids: List[:class:`~melisa.utils.snowflake.Snowflake`]
        List of role ids.
    joined_at: Optional[:class:`~melisa.utils.timestamp.Timestamp`]
        When the user joined the guild
    premium_since: Optional[:class:`~melisa.utils.timestamp.Timestamp`]
        When the user started boosting the guild
    is_deaf: :class:`bool`
        Whether the user is deafened in voice channels
    is_mute: :class:`bool`
        Whether the user is muted in voice channels
    pending: Optional[:class:`bool`]
        the user has not yet passed the guild's Membership Screening requirements
    permissions: Optional[:class:`str`]
        Total permissions of the member in the channel,
        including overwrites, returned when in the interaction object
    communication_disabled_until: Optional[:class:`~melisa.utils.timestamp.Timestamp`]
        When the user's timeout will expire and the user will be able to communicate in the guild again,
        null or a time in the past if the user is not timed out
    guild_id: List[:class:`~melisa.utils.snowflake.Snowflake`]
        The id of the guild this member belongs to.
    """
    user: APINullable[User] = None
    nick: APINullable[str] = None
    guild_avatar: APINullable[str] = None
    role_ids: List[Snowflake] = None
    joined_at: APINullable[Timestamp] = None
    premium_since: APINullable[Timestamp] = None
    is_deaf: bool = None
    is_mute: bool = None
    is_pending: APINullable[bool] = None
    permissions: APINullable[str] = None
    communication_disabled_until: APINullable[Timestamp] = None
    guild_id: APINullable[Snowflake] = None

    def make_guild_avatar_url(self, size: int = 1024) -> str:
        # ToDo: Add extensions parameter
        """User guild avatar url (from the Discord CDN server)

        Parameters
        ----------
        size: int
            The size to set for the URL, defaults to 1024. Can be any power of two between 16 and 4096.
        """
        return "https://cdn.discordapp.com/guilds/{}/users/{}/avatars/{}.png?size={}".format(
            self.guild_id, self.user.id, self.guild_avatar, size
        )

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> GuildMember:
        """Generate a guild member from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a guild member.
        """

        self: GuildMember = super().__new__(cls)

        self.user = User.from_dict(data['user']) if data.get('user') is not None else None
        self.nick = data.get("nick")
        self.guild_avatar = data.get('avatar')
        self.role_ids = [Snowflake(x) for x in data['roles']]
        self.joined_at = Timestamp.parse(data['joined_at']) if data.get('joined_at') is not None else None
        self.premium_since = Timestamp.parse(data['premium_since']) if data.get('premium_since') is not None else None
        self.is_deaf = data.get("deaf")
        self.is_mute = data.get("mute")
        self.is_pending = data.get("pending")
        self.permissions = data.get("permissions")
        self.communication_disabled_until = Timestamp.parse(data['communication_disabled_until']) if data.get('communication_disabled_until') is not None else None
        self.guild_id = data.get("guild_id")

        return self
