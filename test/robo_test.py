
# TODO: import some code

# TODO: test the code

import os
import pytest

from app.my_script import get_response

# expect default environment variable setting of "CI=true" on Travis CI
# see: https://docs.travis-ci.com/user/environment-variables/#default-environment-variables
CI_ENV = os.getenv("CI") == "true"

@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server") # skips this test on CI
def test_get_response():
    symbol = "NFLX"
    parsed_response = get_response(symbol) # issues an HTTP request (see function definition below)

    assert isinstance(parsed_response, dict)
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol
