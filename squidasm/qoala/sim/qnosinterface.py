from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Generator, Optional, Union

from netsquid.components import QuantumProcessor
from netsquid.components.instructions import Instruction as NsInstr
from netsquid.components.qprogram import QuantumProgram

from pydynaa import EventExpression
from squidasm.qoala.sim.common import ComponentProtocol, PortListener
from squidasm.qoala.sim.qnos import QnosComponent
from squidasm.qoala.sim.signals import (
    SIGNAL_HOST_HAND_MSG,
    SIGNAL_MEMORY_FREED,
    SIGNAL_NSTK_PROC_MSG,
)


class QnosInterface(ComponentProtocol):
    """NetSquid protocol representing a QNodeOS processor."""

    def __init__(self, comp: QnosComponent) -> None:
        """Processor protocol constructor. Typically created indirectly through
        constructing a `Qnos` instance.

        :param comp: NetSquid component representing the processor
        :param qnos: `Qnos` protocol that owns this protocol
        """
        super().__init__(name=f"{comp.name}_protocol", comp=comp)
        self._comp = comp

        self.add_listener(
            "host",
            PortListener(self._comp.ports["host_in"], SIGNAL_HOST_HAND_MSG),
        )
        self.add_listener(
            "netstack",
            PortListener(self._comp.ports["nstk_in"], SIGNAL_NSTK_PROC_MSG),
        )

        self.add_signal(SIGNAL_MEMORY_FREED)

    def send_host_msg(self, msg: Any) -> None:
        self._comp.host_out_port.tx_output(msg)

    def receive_host_msg(self) -> Generator[EventExpression, None, str]:
        return (yield from self._receive_msg("host", SIGNAL_HOST_HAND_MSG))

    def send_netstack_msg(self, msg: str) -> None:
        self._comp.netstack_out_port.tx_output(msg)

    def receive_netstack_msg(self) -> Generator[EventExpression, None, str]:
        return (yield from self._receive_msg("netstack", SIGNAL_NSTK_PROC_MSG))

    def flush_netstack_msgs(self) -> None:
        self._listeners["netstack"].buffer.clear()

    @property
    def qdevice(self) -> QuantumProcessor:
        return self._comp.qdevice
