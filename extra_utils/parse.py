import re
import logging

from typing import Dict, Match, Optional


logger = logging.getLogger(__name__)


regex = (
    r'((?P<weeks>\d+?)w)?'
    r'((?P<days>\d+?)d)?'
    r'((?P<hours>\d+?)h)?'
    r'((?P<minutes>\d+?)m)?'
    r'((?P<seconds>\d+?)s)?'
)


def parse_time(time_str: str):
    pattern = re.compile(regex)
    result: Optional[Match[str]] = pattern.match(time_str)
    logger.debug(result)
    if not result:
        return
    parts: Dict[str, str] = result.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return time_params
