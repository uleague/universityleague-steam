class FakeUser:
    def __init__(self):
        self.name = "ULeague"
        self.friends = [FakeFriend() for i in range(20)]
        self.id64 = 123
        self.avatar_url = "avatar_url"

    async def add(self):
        return

    async def send(self, message):
        return


class FakeFriend(FakeUser):
    def __init__(self):
        self.id64 = 123
        self.name = "Fake Friend"


class FakeSteam(FakeUser):
    def __init__(self):
        self.user = FakeUser()

    async def fetch_user(self, steam_id):
        if isinstance(steam_id, int):
            return FakeUser()
