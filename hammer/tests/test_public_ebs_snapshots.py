from . import mock_ebs
from library.aws.ebs import EBSPublicSnapshotsChecker
from library.aws.utility import Account


region = "us-east-1"
availability_zone = "us-east-1a"

ebs_volumes = {
"Volume1":{
        "Description": "Volume",
        "AvailabilityZone": availability_zone,
        "Encrypted": False,
        "CheckShouldPass": False
    },
"Volume2":{
        "Description": "Volume",
        "AvailabilityZone": availability_zone,
        "Encrypted": True,
        "CheckShouldPass": False
    }
}

ebs_snapshots = {
    "Snapshot1":{
        "Description": "Public snapshot",
        "Volume": "Volume1",
        "IsPublicSnapshot": True,
        "CheckShouldPass": False
    },
    "Snapshot2":{
        "Description": "Private snapshot",
        "Volume": "Volume2",
        "IsPublicSnapshot": False,
        "CheckShouldPass": True
    },
}

def find_snapshot_name(snapshot):
    for name, props in ebs_snapshots.items():
        if props["Id"] == snapshot.id:
            return name
    return None

def find_rule_prop(snapshot, prop, default):
    name = find_snapshot_name(snapshot)
    return ebs_snapshots.get(name, {}).get(prop, default)

def ident_snapshot_test(arg):
    """
    Used to build identification string for each autogenerated test (for easy recognition of failed tests).

    :param arg: dict with information about rules.
    :return: identification string with snapshot_id.
    """
    if isinstance(arg, bool):
        return "remediated" if arg else "original"
    else:
        name = find_snapshot_name(arg)
        descr = find_rule_prop(arg, "Description", "default description")
        return f"params: {name} ({descr})"

def pytest_generate_tests(metafunc):
    """
    Entrypoint for tests (built-in pytest function for dynamic generation of test cases).
    """
    # Launch EC2 mocking and env preparation
    mock_ebs.start()
    mock_ebs.create_env_volumes(ebs_volumes, region)
    mock_ebs.create_env_snapshots(ebs_volumes, ebs_snapshots, region)

    account = Account(region=region)

    # validate ebs snapshots in mocked env
    checker = EBSPublicSnapshotsChecker(account)
    checker.check()

    for ec2_snapshot in checker.snapshots:
        ec2_snapshot.make_private()

    checker_remediated = EBSPublicSnapshotsChecker(account)
    checker_remediated.check()

    snapshots_list = [(snapshot, False) for snapshot in checker.snapshots]
    snapshots_list += [(snapshot, True) for snapshot in checker_remediated.snapshots]
    # create test cases for each response
    metafunc.parametrize("snapshot,remediated", snapshots_list, ids=ident_snapshot_test)


def test_snapshots(snapshot, remediated):
    """
    Actual testing function.

    :param snapshot: dict with information about rules
    :param remediated:  
    :return: nothing, raises AssertionError if actual test result is not matched with expected
    """
    expected = True if remediated else find_rule_prop(snapshot, "CheckShouldPass", True)
    assert expected == (not snapshot.public)
