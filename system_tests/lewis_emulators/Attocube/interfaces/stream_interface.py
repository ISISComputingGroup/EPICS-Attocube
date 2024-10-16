import logging
import typing

from lewis.adapters.stream import StreamInterface  #  type: ignore
from lewis.core.logging import has_log  #  type: ignore
from lewis.utils.command_builder import CmdBuilder  #  type: ignore

if typing.TYPE_CHECKING:
    from lewis_emulators.Attocube.device import SimulatedAttocube


@has_log
class AttocubeStreamInterface(StreamInterface):
    in_terminator = "\r\n"
    out_terminator = "\r\n:"
    readtimeout = 100

    def __init__(self) -> None:
        super(AttocubeStreamInterface, self).__init__()
        self.device: "SimulatedAttocube"
        self.log: "logging.Logger"
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_angle).escape("ATANGLE=").eos().build(),
            CmdBuilder(self.set_angle_val).escape("ATTO=").float().eos().build(),
            CmdBuilder(self.set_angle_go).escape("ATGO=1").eos().build(),
            CmdBuilder(self.get_ark).escape("Y=").eos().build(),
            CmdBuilder(self.set_ark_val).escape("ARK=").float().eos().build(),
            CmdBuilder(self.set_ark_go).escape("ARGO=1").eos().build(),
            CmdBuilder(self.count_verbose).escape("VERBOSE=0").eos().build(),
            CmdBuilder(self.count_ab0).escape("AB0").eos().build(),
            CmdBuilder(self.count_mo).escape("MO").eos().build(),
            CmdBuilder(self.count_xq).escape("XQ #SXD").eos().build(),
            CmdBuilder(self.count_mg).escape('MG "stop 1" {P2}').eos().build(),
            CmdBuilder(self.get_busy).escape("BUSY=").eos().build(),
        }

    def handle_error(self, request: str, error: str | Exception) -> None:
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_angle(self) -> str:
        return f"{self.device.angle}"

    def set_angle_val(self, angle_sp: float) -> None:
        self.device.angle_val = angle_sp

    def set_angle_go(self) -> None:
        if self.device.angle_val is None:
            self.log.error("ATGO was recieved before angle had been set")
        else:
            self.device.angle = self.device.angle_val

    def get_ark(self) -> str:
        return f"{self.device.ark}"

    def set_ark_val(self, ark_sp: float) -> None:
        self.device.ark_val = ark_sp

    def set_ark_go(self) -> None:
        if self.device.ark_val is None:
            self.log.error("ARGO was recieved before ark had been set")
        else:
            self.device.ark = self.device.ark_val

    def count_verbose(self) -> None:
        self.device.verbose_count += 1

    def count_ab0(self) -> None:
        self.device.ab0_count += 1

    def count_mo(self) -> None:
        self.device.mo_count += 1

    def count_xq(self) -> None:
        self.device.xq_count += 1

    def count_mg(self) -> None:
        self.device.mg_count += 1

    def get_busy(self) -> str:
        if self.device.busy:
            return "1.0000"
        else:
            return "0.0000"
