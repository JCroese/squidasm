from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional, Type

from netqasm.backend.messages import StopAppMessage, SubroutineMessage
from netqasm.lang.operand import Register
from netqasm.lang.parsing.text import NetQASMSyntaxError, parse_register
from netqasm.sdk.transpile import NVSubroutineTranspiler, SubroutineTranspiler
from netsquid.components.component import Component, Port
from netsquid.nodes import Node

from pydynaa import EventExpression
from squidasm.qoala.lang import iqoala
from squidasm.qoala.lang.iqoala import IqoalaProgram
from squidasm.qoala.runtime.environment import GlobalEnvironment, LocalEnvironment
from squidasm.qoala.runtime.program import BatchResult, ProgramContext, ProgramInstance
from squidasm.qoala.sim.common import ComponentProtocol, PortListener
from squidasm.qoala.sim.csocket import ClassicalSocket
from squidasm.qoala.sim.hostcomp import HostComponent
from squidasm.qoala.sim.hostprocessor import HostProcessor, IqoalaProcess
from squidasm.qoala.sim.interfaces import HostInterface
from squidasm.qoala.sim.logging import LogManager
from squidasm.qoala.sim.memory import ProgramMemory, UnitModule
from squidasm.qoala.sim.signals import SIGNAL_HAND_HOST_MSG, SIGNAL_HOST_HOST_MSG
from squidasm.qoala.sim.util import default_nv_unit_module


class Host(ComponentProtocol):
    """NetSquid protocol representing a Host."""

    def __init__(
        self,
        comp: HostComponent,
        local_env: LocalEnvironment,
        qdevice_type: Optional[str] = "nv",
    ) -> None:
        """Host protocol constructor.

        :param comp: NetSquid component representing the Host
        :param qdevice_type: hardware type of the QDevice of this node
        """
        super().__init__(name=f"{comp.name}_protocol", comp=comp)
        self._comp = comp
        self._interface = HostInterface(comp, local_env)

        self._processor = HostProcessor(self)

    @property
    def processor(self) -> HostProcessor:
        return self._processor

    @property
    def local_env(self) -> LocalEnvironment:
        return self._local_env

    def run_iqoala_instr(
        self, process: IqoalaProcess, instr_idx: int
    ) -> Generator[EventExpression, None, None]:
        yield from process.run(instr_idx)

    def program_end(self, pid: int) -> BatchResult:
        self.send_qnos_msg(bytes(StopAppMessage(pid)))
        return self._processes[pid].get_results()

    def run_process(self, pid: int) -> None:
        pass

    def get_results(self) -> List[Dict[str, Any]]:
        return self._program_results

    def start(self) -> None:
        assert self._interface is not None
        super().start()
        self._interface.start()

    def stop(self) -> None:
        self._interface.stop()
        super().stop()
