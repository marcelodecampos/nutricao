"""modulo responsavel pelas variaveis de ambiente"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

MB = 1024 * 1024


class PostgresSettings(BaseSettings):
    """
    Parses variables from environment on instantiation
    if url is set hostname, port and db are ignored
    """

    model_config: SettingsConfigDict = SettingsConfigDict(
        validate_default=False, env_prefix="PG_", env_file=".env", extra="ignore"
    )
    url: str = Field(default=None)
    username: str = Field(default="postgres")
    password: SecretStr = Field(default=SecretStr("curiosidade matou o gato"))
    hostname: str = Field(default="db.local")
    port: int = Field(default=5432)
    db: str = Field(default="sistema")
    driver: str = Field(default="psycopg")
    params: str = Field(default=None)

    """
    if True, the Engine will log all statements as well as a repr()
    of their parameter lists to the default log handler
    """
    log_all_statements: bool = Field(default=True)

    """
    if True, the connection pool will log informational output such as when
    connections are invalidated as well as when connections are recycled to the
    default log handler, which defaults to sys.stdout for output
    """
    log_pool_informaton: bool = Field(default=True)

    """
    the number of connections to allow in connection pool “overflow”, that is
    connections that can be opened above and beyond the pool_size setting,
    which defaults to five. this is only used with QueuePool
    """
    max_overflow: int = Field(default=5)

    """
    if True will enable the connection pool “pre-ping” feature that tests
    connections for liveness upon each checkout
    """
    pool_pre_ping: bool = Field(default=True)

    """the number of connections to keep open inside the connection pool."""
    pool_size: int = Field(default=30)

    """
    use LIFO (last-in-first-out) when retrieving connections from QueuePool
    instead of FIFO (first-in-first-out)
    """
    pool_use_lifo: bool = Field(default=True)

    @property
    def uri(self) -> str:
        """Build postgresql uri to connect using SQLAlchemy"""
        db_envs: PostgresSettings = envs.db
        uri_template: str = "postgresql+{}://{}:{}@{}:{}/{}"

        driver = db_envs.driver

        postgres_uri = (
            db_envs.url
            if db_envs.url
            # pylint:disable=no-member
            else uri_template.format(
                driver,
                db_envs.username,
                db_envs.password.get_secret_value(),
                db_envs.hostname,
                db_envs.port,
                db_envs.db,
            )
        )
        if db_envs.params:
            postgres_uri += "?" + db_envs.params
        return postgres_uri


class EnvironmentSettings(BaseSettings):
    """inner class to load all parameters"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        validate_default=False, env_file=".env", extra="ignore"
    )
    db: PostgresSettings = PostgresSettings()

    tz: str = Field(default="America/Sao_Paulo")
    debug: bool = Field(default=False)
    trace_http_headers: bool = Field(default=False)
    service_endpoint: str = Field(default="/jcr-storage-server/documents/{nr_document_storage}")
    time_middleware: bool = Field(default=False)
    prometheus: bool = Field(default=True)
    health_checks: bool = Field(default=True)
    openapi_url: str = Field(default="/openapi.json")
    allow_origins: str = Field(default='["*"]')
    allow_credentials: bool = Field(default=True)
    use_cors: bool = Field(default=False)
    allow_methods: str = Field(default='["*"]')
    allow_headers: str = Field(default='["*"]')
    use_rate_limit: bool = Field(default=False)
    rate_limit_max_requests: int = Field(default=50)
    rate_limit_window: int = Field(default=1)
    chunk_size: int = Field(default=4 * MB)
    allow_invalid_hash: bool = Field(default=False)


envs = EnvironmentSettings()


def run():
    """Test only"""
    env = EnvironmentSettings()
    from pprint import pprint  # pylint: disable=import-outside-toplevel

    pprint(env.model_dump())
    _uri = envs.db.uri
    pprint(f"Database uri: f{_uri}")


if __name__ == "__main__":
    run()
