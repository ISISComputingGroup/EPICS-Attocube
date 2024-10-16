import unittest

from utils.channel_access import ChannelAccess  #  type: ignore
from utils.ioc_launcher import get_default_ioc_dir  #  type: ignore
from utils.test_modes import TestModes  #  type: ignore
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim  #  type: ignore

DEVICE_PREFIX = "ATTOCUBE_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("ATTOCUBE"),
        "macros": {},
        "emulator": "Attocube",
    },
]


TEST_MODES = [TestModes.RECSIM, TestModes.DEVSIM]


class AttocubeTests(unittest.TestCase):
    """
    Tests for the Attocube IOC.
    """

    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Attocube", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)

    def test_that_dissable_pv_IS_ENABLED(self):
        self.ca.assert_that_pv_is("DISABLE", "COMMS ENABLED")

    def test_WHEN_angle_set_THEN_ioc_reads_angle(self):
        self.ca.assert_setting_setpoint_sets_readback(-20, "ANGLE")

    def test_WHEN_ark_set_THEN_ioc_reads_ark(self):
        self.ca.assert_setting_setpoint_sets_readback(-15, "ARK")

    @skip_if_recsim("makes use of backdoor")
    def test_WHEN_initialised_THEN_correct_comands_sent(self):
        # Given current count of comands recieved by emulator
        self.verbose_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("verbose_count"))
        self.ab0_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("ab0_count"))
        self.mo_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("mo_count"))
        self.xq_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("xq_count"))
        self.mg_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("mg_count"))

        # When initialisation PV processed
        self.ca.process_pv("INIT")

        # Then assert count of comands recieved by emulator increases by 1
        self._lewis.assert_that_emulator_value_is(
            "verbose_count", str(self.verbose_count_backdoor_pre + 1)
        )
        self._lewis.assert_that_emulator_value_is("ab0_count", str(self.ab0_count_backdoor_pre + 1))
        self._lewis.assert_that_emulator_value_is("mo_count", str(self.mo_count_backdoor_pre + 1))
        self._lewis.assert_that_emulator_value_is("xq_count", str(self.xq_count_backdoor_pre + 1))
        self._lewis.assert_that_emulator_value_is("mg_count", str(self.mg_count_backdoor_pre + 1))

    @skip_if_recsim("makes use of backdoor")
    def test_WHEN_stopped_THEN_correct_comands_sent(self):
        # Given current count of comands recieved by emulator
        self.ab0_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("ab0_count"))
        self.mo_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("mo_count"))
        self.xq_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("xq_count"))
        self.mg_count_backdoor_pre = int(self._lewis.backdoor_get_from_device("mg_count"))

        # When initialisation PV processed
        self.ca.process_pv("STOP")

        # Then assert count of comands recieved by emulator increases by 1
        self._lewis.assert_that_emulator_value_is("ab0_count", str(self.ab0_count_backdoor_pre + 1))
        self._lewis.assert_that_emulator_value_is("mo_count", str(self.mo_count_backdoor_pre + 1))
        self._lewis.assert_that_emulator_value_is("xq_count", str(self.xq_count_backdoor_pre + 1))
        self._lewis.assert_that_emulator_value_is("mg_count", str(self.mg_count_backdoor_pre + 1))

    @skip_if_recsim("makes use of backdoor")
    def test_WHEN_busy_THEN_reports_busy(self):
        # Given emulator set to be busy
        self._lewis.backdoor_set_on_device("busy", True)

        # Then BUSY PV reports busy
        self.ca.assert_that_pv_is("BUSY", "BUSY")

    @skip_if_recsim("makes use of backdoor")
    def test_WHEN_not_busy_THEN_not_busy(self):
        # Given emulator set to be not busy
        self._lewis.backdoor_set_on_device("busy", False)

        # Then BUSY PV reports not busy
        self.ca.assert_that_pv_is("BUSY", "NOT BUSY")
