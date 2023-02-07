import motor.motor_asyncio
import pytest
from _pytest.config.argparsing import Parser
from pydantic import BaseSettings


class Settings(BaseSettings):
    mongodb_dsn: str = "mongodb://test:test@localhost:27017/admin"
    mongodb_db_name: str = "beanie_db"


@pytest.hookimpl(optionalhook=True)
def pytest_addoption(parser: Parser):
    parser.addoption("--testcontainer", action="store", default=False)


@pytest.fixture(scope="session")
def testcontainer(pytestconfig):
    option_value: bool = pytestconfig.getoption("testcontainer")
    if option_value == "True":
        from testcontainers.mongodb import MongoDbContainer

        with MongoDbContainer("mongo:latest").with_bind_ports(
            27017, 27017
        ) as mongo:
            yield mongo


@pytest.fixture
def settings(testcontainer):
    return Settings()


@pytest.fixture()
def cli(settings, loop):
    return motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_dsn)


@pytest.fixture()
def db(cli, settings, loop):
    return cli[settings.mongodb_db_name]
