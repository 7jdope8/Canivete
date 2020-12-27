import pytest


from . import mock_iam
from datetime import datetime, timedelta, timezone
from library.aws.iam import IAMKeyChecker
from library.aws.utility import Account


# starting point for checking if key expired
now = datetime.now(timezone.utc)
# criteria for checking if key expired
inactive_criteria_days = timedelta(days=10)

# mocked AWS IAM environment
users = {
    "User1": {
        "Keys": [
            {
                "Description": "Key on a half way to expiration",
                "LastUsed": now - inactive_criteria_days / 2,
                "Active": True,
                "CheckShouldPass": True
            },
            {
                "Description": "Key with one day before expiration",
                "LastUsed": now - inactive_criteria_days + timedelta(days=1),
                "Active": True,
                "CheckShouldPass": True
            },
            {
                "Description": "Not used key expired one minute ago",
                "LastUsed": None,
                "CreateDate": now - inactive_criteria_days - timedelta(minutes=1),
                "Active": True,
                "CheckShouldPass": False
            },
            {
                "Description": "Not active key",
                "Active": False,
                "CheckShouldPass": True
            }
        ]
    },
    "User2": {
        "Keys": [
            {
                "Description": "Key with one minute before expiration",
                "LastUsed": now - inactive_criteria_days + timedelta(minutes=1),
                "Active": True,
                "CheckShouldPass": True
            },
            {
                "Description": "Key expired one minute ago",
                "LastUsed": now - inactive_criteria_days - timedelta(minutes=1),
                "Active": True,
                "CheckShouldPass": False
            },
            {
                "Description": "Not used key with one minute before expiration",
                "LastUsed": None,
                "CreateDate": now - inactive_criteria_days + timedelta(minutes=1),
                "Active": True,
                "CheckShouldPass": True
            }
        ]
    }
}


def ident_test(key):
    """
    Used to build identification string for each autogenerated test (for easy recognition of failed tests).

    :param keyInactive_details: dict with information about access key from
                        describe_iam_accesskeyInactive_details.validate_user_inactive_keys(...)
    :return: identification string with user name, key index number and human-readable description.
    """
    descr = mock_iam.find_key_prop(users, key, "Description", "default description")
    indx = mock_iam.find_key_prop(users, key, "TestId", "0")
    return f"params: {key.user.id}.{indx} ({descr})"


def pytest_generate_tests(metafunc):
    """
    Entrypoint for tests (built-in pytest function for dynamic generation of test cases).
    """
    # Launch IAM mocking and env preparation
    mock_iam.start()
    mock_iam.create_env(users)

    account = Account()

    # validate user inactive keys in mocked env
    checker = IAMKeyChecker(account,
                            now=now,
                            inactive_criteria_days=inactive_criteria_days)
    checker.check(last_used_check_enabled=True)
    keys = []
    for user in checker.users:
        keys += user.keys

    # create test cases for each key
    metafunc.parametrize("key", keys, ids=ident_test)


@pytest.mark.iamInactive
def test_keyInactive(key):
    """
    Actual testing function.

    :param keyInactive_details: dict with information about access key from
                        describe_iam_accesskeyInactive_details.validate_user_inactive_keys(...)
    :return: nothing, raises AssertionError if actual test result is not matched with expected
    """
    #print(f"{json.dumps(keyInactive_details, indent=4, default = jsonEncoder)}")
    expected = mock_iam.find_key_prop(users, key, "CheckShouldPass", True)
    assert expected == (not key.inactive)