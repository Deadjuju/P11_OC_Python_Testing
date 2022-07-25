from locust import HttpUser, task

from tests.conftest import Urls


club = {
    "name":"Simply Lift",
    "email":"john@simplylift.co",
    "points":"13"
}
competition = {
    "name": "Super Smash Force",
    "date": "3000-10-22 13:30:00",
    "numberOfPlaces": "18"
}


class SitePerfTest(HttpUser):

    def on_start(self):
        self.client.get(Urls.INDEX.value)

    @task
    def index(self):
        self.client.get(Urls.INDEX.value)

    @task
    def login(self):
        self.client.post(Urls.LOGIN.value, {"email": club['email']})

    @task
    def bad_login(self):
        self.client.post(Urls.LOGIN.value, {"email": "wrong_email@mail.com"})

    @task
    def book(self):
        self.client.get(Urls.booking_url(competition=competition['name'],
                                         club=club['name']))

    @task
    def purchase_places(self):
        data_to_post = {
            'club': club['name'],
            'competition': competition['name'],
            'places': 1,
        }
        self.client.post(Urls.PURCHASE_PLACES.value, data=data_to_post)

    @task
    def view_display_board(self):
        self.client.get(Urls.DISPLAY_BOARD.value)

    @task
    def logout(self):
        self.client.get(Urls.LOGOUT.value)
