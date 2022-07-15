from datetime import datetime


class ClubNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


class CompetitionNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NegativeResultError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_club_by_key(club_list: list[dict], club_info: str, key: str) -> dict:
    """ find a club

    Args:
        club_list (list): list of registered clubs
        club_info (str): club information used to get it (club name or club mail)
        key (str): dictionary key used to retrieve the club ('name' or 'email')

    Returns:
        dict: full club information
    """
    for club in club_list:
        if club[key] == club_info:
            return club
    message = f"No correspondence with this {key}."
    raise ClubNotFoundError(message)


def get_competition(competitions_list: list[dict], competition_name: str) -> dict:
    """ find a competition

    Args:
        competitions_list (list): list of registered competitions
        competition_name (str): competition name

    Returns:
        dict: full competition information
    """

    for competition in competitions_list:
        if competition['name'] == competition_name:
            return competition
    message = f"No correspondence with this name."
    raise CompetitionNotFoundError(message)


def is_date_not_already_past(date: str) -> bool:
    """ determines if a date has not yet passed

    Args:
        date (str): date to compare

    Returns:
        bool: TRUE if the date is in the future, else FALSE
    """
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return bool(date > today)


def update_points_or_places(places_required: int, current_points_or_places: int) -> int:
    """
    Updates the number of points of a club or the number of places remaining in a competition,
    if the number is not positive raise an exception.
    """
    update_result = current_points_or_places - places_required
    if update_result < 0:
        raise NegativeResultError("Negative values are not allowed")
    return update_result


def init_a_club_if_not_in_dict(club_places_per_competition: dict, club_name: str):
    """
    add a club in club_places_per_competition if it is not yet present
    """
    if club_places_per_competition.get(club_name) is None:
        club_places_per_competition[club_name] = {}


def _update_club_competitions_and_places(club_competitions_and_places,
                                         competition_name,
                                         current_places_competition,
                                         required_places):
    """ Update the dictionnary

    Args:
        club_places_per_competition (dict):
        club_name (str): name of current club
        competition_name (str): name of current competition
        required_places (int): number of places requested
    """

    club_competitions_and_places[competition_name] = (current_places_competition + required_places)


def check_places_number_for_a_competition_and_update(club_places_per_competition: dict,
                                                     club_name: str,
                                                     competition_name: str,
                                                     required_places: int) -> bool:
    """ Checks if the number of places reserved for a competition is less than or equal to 12.
    The club_places_per_competition dictionary is updated if True

    Args:
        club_places_per_competition (dict):
        club_name (str): name of current club
        competition_name (str): name of current competition
        required_places (int): number of places requested

    Returns:
        bool: False if places > 12, else True
    """


    club_competitions_and_places: dict = club_places_per_competition.get(club_name)
    current_places_competition = club_competitions_and_places.get(competition_name, 0)
    if current_places_competition + required_places > 12:
        return False

    _update_club_competitions_and_places(club_competitions_and_places,
                                         competition_name,
                                         current_places_competition,
                                         required_places)
    return True
