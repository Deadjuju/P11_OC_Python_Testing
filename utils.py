from datetime import datetime


def is_date_not_already_past(date: str) -> bool:
    """determines if a date has not yet passed

    Args:
        date (str): date to compare

    Returns:
        bool: TRUE if the date is in the future, else FALSE
    """
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return bool(date > today)
