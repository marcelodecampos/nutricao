import reflex as rx

config = rx.Config(
    app_name="nutricao",
    db_url="postgresql+psycopg://postgres:curiosidade@db.local:5432/minhanutri?application_name=relfex",
    frontend_port=3000,
    backend_port=8080,
    loglevel="debug",
)
