def setup_index_handler(app, handler):
    app.router.add_get(
        "/", handler.index, name="index",
    )


def setup_friends_handler(app, handler):
    app.router.add_get("/friends", handler.get_friends, name="get_friends")
    app.router.add_post("/friends", handler.post_friends, name="post_friends")


def setup_message_handler(app, handler):
    app.router.add_post("/message", handler.post_message, name="post_message")
