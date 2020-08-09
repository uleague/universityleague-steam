class ULeagueRequestError(Exception):
    """
    Basic exception for all requests
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "Произошла ошибка во время выполнения запроса на ULeague --> {}".format(
            self.message
        )
