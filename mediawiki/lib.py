
import aiohttp
import asyncio

from urllib.parse import urlencode
from typing import Union
from typing import Optional
from typing import overload
from collections.abc import Iterable

EN_WIKIPEDIA_ENDPOINT = "https://en.wikipedia.org/w/api.php?"

def _join_params(params: Iterable[str]) -> str:
    # FIXME: if params need to have '|' in them, use other seperation method according to information here:
    # https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatypes
    # also, prevent '\u001F' from being in params, because that is (implicitly) disallowed by the mediawiki
    # rules.
    return '|'.join(params)

@overload
async def summary(titles: str) -> Optional[str]:
    ...

@overload
async def summary(titles: list[str]) -> dict[str, Optional[str]]:
    ...

async def summary(titles: Union[str, list[str]]) -> Union[Optional[str], dict[str, Optional[str]]]:
    call = {
        'action' : 'query',
            'prop' : 'extracts',
                'exintro' : True,
                'explaintext' : True,
            'titles' : titles if type(titles) is str else _join_params(titles),
        'format' : 'json',
    }
    async with aiohttp.ClientSession() as session, session.get(EN_WIKIPEDIA_ENDPOINT + urlencode(call)) as response:
        return await response.json()
