
from netsquid.nodes import Node
from netsquid.components import QuantumProcessor, PhysicalInstruction
from netsquid.components.instructions import (
    INSTR_INIT,
    INSTR_X,
    INSTR_Y,
    INSTR_Z,
    INSTR_H,
    INSTR_K,
    INSTR_S,
    INSTR_T,
    INSTR_CNOT,
    INSTR_CZ,
)


def get_node(name, node_id=None, num_qubits=5):
    qdevice = get_qdevice(name=f"{name}_QPD", num_qubits=num_qubits)
    node = Node(name, ID=node_id, qmemory=qdevice)

    return node


def get_nodes(names, node_ids=None, num_qubits=5):
    if node_ids is None:
        node_ids = list(range(len(names)))
    assert len(names) == len(node_ids), "Wrong number of node IDs"
    nodes = {}
    for name, node_id in zip(names, node_ids):
        nodes[name] = get_node(name=name, node_id=node_id, num_qubits=num_qubits)

    return nodes


def get_qdevice(name="QPD", num_qubits=5):
    return QuantumProcessor(name=name, num_positions=num_qubits, phys_instructions=[
        # TODO durations (currently arbitary)
        PhysicalInstruction(INSTR_INIT, duration=1),
        PhysicalInstruction(INSTR_X, duration=2),
        PhysicalInstruction(INSTR_Y, duration=2),
        PhysicalInstruction(INSTR_Z, duration=2),
        PhysicalInstruction(INSTR_H, duration=3),
        PhysicalInstruction(INSTR_K, duration=3),
        PhysicalInstruction(INSTR_S, duration=3),
        PhysicalInstruction(INSTR_T, duration=4),
        PhysicalInstruction(INSTR_CNOT, duration=5),
        PhysicalInstruction(INSTR_CZ, duration=5),
    ])
