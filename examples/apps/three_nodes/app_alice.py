from netqasm.sdk import EPRSocket
from squidasm.sdk import NetSquidConnection

from netqasm.logging import get_netqasm_logger

logger = get_netqasm_logger()


def main(app_config=None):
    epr_socket_bob = EPRSocket(
        remote_node_name="bob",
        epr_socket_id=0,
        remote_epr_socket_id=0
    )
    epr_socket_charlie = EPRSocket(
        remote_node_name="charlie",
        epr_socket_id=1,
        remote_epr_socket_id=0
    )

    node_name = app_config.node_name
    if node_name is None:
        node_name = app_config.app_name

    alice = NetSquidConnection(
        node_name=node_name,
        log_config=app_config.log_config,
        epr_sockets=[epr_socket_bob, epr_socket_charlie]
    )
    with alice:
        epr_bob = epr_socket_bob.create()[0]
        m_bob = epr_bob.measure()

        alice.flush()

        epr_charlie = epr_socket_charlie.create()[0]
        m_charlie = epr_charlie.measure()

    logger.info(f"alice:    m_bob:    {m_bob}")
    logger.info(f"alice:    m_charlie:{m_charlie}")


if __name__ == "__main__":
    main()
