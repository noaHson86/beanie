import random
import string

import pytest

from beanie import WriteRules
from tests.odm.models import Post, Picture, GenericFile


@pytest.fixture
def random_word(length: int = 8):
    return "".join(
        random.choice(string.ascii_lowercase) for _ in range(length)
    )


@pytest.fixture
def get_picture():
    return Picture(file=GenericFile())


@pytest.fixture
def post_with_everything(random_word, get_picture):
    return Post(text=random_word, picture=get_picture)


class TestFetch:
    async def test_fetch_nested(self, post_with_everything):
        res: Post = await post_with_everything.insert(
            link_rule=WriteRules.WRITE
        )
        assert res.id
