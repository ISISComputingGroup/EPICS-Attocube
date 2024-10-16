from collections import OrderedDict

from lewis.devices import StateMachineDevice  #  type: ignore

from .states import DefaultState


class SimulatedAttocube(StateMachineDevice):
    def _initialize_data(self) -> None:
        # Ark
        self.angle: float = 0
        # Angle as recieved by emulator, angle only set when go comand recieved
        self.angle_val: float | None = None

        # Angle
        self.ark: float = 0
        # Ark as recieved by emulator, ark only set when go comand recieved
        self.ark_val: float | None = None

        # Initialisation and Stop comand recieved counters
        self.verbose_count = 0
        self.ab0_count = 0
        self.mo_count = 0
        self.xq_count = 0
        self.mg_count = 0

        # Busy
        self.busy = False

    def _get_state_handlers(self) -> dict:
        return {
            "default": DefaultState(),
        }

    def _get_initial_state(self) -> str:
        return "default"

    def _get_transition_handlers(self) -> dict:
        return OrderedDict([])
