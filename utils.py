from datetime import datetime


class ClubNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_club_by_key(club_list: list[dict], club_info: str, key: str) -> dict:
    """
    Find a club
    """
    for club in club_list:
        if club[key] == club_info:
            return club
    message = f"No correspondence with this {key}."
    raise ClubNotFoundError(message)


def is_date_not_already_past(date: str) -> bool:
    """determines if a date has not yet passed

    Args:
        date (str): date to compare

    Returns:
        bool: TRUE if the date is in the future, else FALSE
    """
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return bool(date > today)
