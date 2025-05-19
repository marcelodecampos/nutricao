"""reflex config module"""

# pylint: disable=not-callable
import reflex as rx


from sqlalchemy import URL

url_object = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password="Curiosity killed the cat",  # plain (unescaped) text
    host="db.local",
    database="minhanutri",
    query={
        "application_name": "reflex",
    },
).render_as_string(False)


config = rx.Config(
    app_name="nutricao",
    db_url=url_object,
    async_db_url=url_object,
    redis_url="redis://db.local:6379/0[&health_check_interval=10&retry_on_timeout=False]",
    frontend_port=3000,
    backend_port=8080,
    loglevel="info",
    state_manager_mode=rx.constants.StateManagerMode.REDIS,
    echo="true",
    echo_pool="true",
    hide_parameters="false",
    pool_pre_ping="true",
    pool_size="30",
    max_overflow="5",
)
