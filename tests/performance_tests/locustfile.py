import pprint

from locust import HttpUser, task


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
        self.client.get("/")

    # def on_stop(self):
    #     self.client.get("logout")

    @task
    def index(self):
        self.client.get("/")

    @task(3)
    def purchase_places(self):
        self.client.post("showSummary", {"email": club['email']})
        self.client.get(f"/book/{competition['name']}/{club['name']}")
        data_to_post = {
            'club': club['name'],
            'competition': competition['name'],
            'places': 1,
        }
        self.client.post('/purchasePlaces', data=data_to_post)

    @task
    def view_display_board(self):
        self.client.get("/points-display-board")

    # @task()
    # def login(self):
    #     valid_mail = "john@simplylift.co"
    #     self.client.post("/showSummary", data={'email': valid_mail})
