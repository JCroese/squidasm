from dataclasses import dataclass
from typing import Dict

from squidasm.qoala.lang.iqoala import IqoalaSubroutine
from squidasm.qoala.runtime.program import ProgramInstance, ProgramResult
from squidasm.qoala.sim.csocket import ClassicalSocket
from squidasm.qoala.sim.eprsocket import EprSocket
from squidasm.qoala.sim.memory import HostMemory, ProgramMemory, SharedMemory


@dataclass
class IqoalaProcess:
    prog_instance: ProgramInstance

    # Mutable
    prog_memory: ProgramMemory
    result: ProgramResult

    # Immutable
    csockets: Dict[int, ClassicalSocket]
    epr_sockets: Dict[int, EprSocket]
    subroutines: Dict[str, IqoalaSubroutine]

    @property
    def pid(self) -> int:
        return self.prog_instance.pid

    @property
    def host_mem(self) -> HostMemory:
        return self.prog_memory.host_mem

    @property
    def shared_mem(self) -> SharedMemory:
        return self.prog_memory.shared_mem
