from typing import Union
import pytz

class InvalidTimezoneError(Exception):
    """Custom exception for invalid timezone errors"""
    pass

def validate_timezone(timezone: Union[str, pytz.tzinfo.BaseTzInfo]) -> pytz.tzinfo.BaseTzInfo:
    """
    Validates that a timezone is a valid pytz timezone.
    
    Args:
        timezone: String timezone name or pytz timezone object
        
    Returns:
        pytz.tzinfo.BaseTzInfo object if valid
        
    Raises:
        InvalidTimezoneError: If timezone is not valid pytz timezone
    """
    if isinstance(timezone, pytz.tzinfo.BaseTzInfo):
        return timezone
        
    if not isinstance(timezone, str):
        raise InvalidTimezoneError("Timezone must be a string or pytz timezone object")
        
    try:
        return pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        raise InvalidTimezoneError(
            f"Invalid timezone '{timezone}'. Must be a valid pytz timezone. "
            "See https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 "
            "for valid timezone names."
        )
