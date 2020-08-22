def setup_index_handler(app, handler):
    app.router.add_get(
        "/", handler.index, name="index",
    )
