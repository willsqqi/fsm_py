import sys
from transitions import Machine, MachineError

VALID_EVENTS = {
    'PASSIVE', 'ACTIVE', 'SYN', 'SYNACK', 'ACK',
    'RDATA', 'SDATA', 'FIN', 'CLOSE', 'TIMEOUT'
}


class TCPFSM:

    states = [
        'CLOSED', 'LISTEN', 'SYN_SENT', 'SYN_RCVD', 'ESTABLISHED',
        'FIN_WAIT_1', 'FIN_WAIT_2', 'CLOSING', 'CLOSE_WAIT', 'LAST_ACK', 'TIME_WAIT'
    ]

    def __init__(self):
        self.data_count = 0
        self.machine = Machine(
            model=self,
            states=TCPFSM.states,
            initial='CLOSED',
            send_event=True,
            ignore_invalid_triggers=False,
        )

        self.machine.add_transition('PASSIVE', 'CLOSED', 'LISTEN', after='log_transition')
        self.machine.add_transition('ACTIVE', 'CLOSED', 'SYN_SENT', after='log_transition')
        self.machine.add_transition('SYN', 'LISTEN', 'SYN_RCVD', after='log_transition')
        self.machine.add_transition('SYN', 'SYN_SENT', 'SYN_RCVD', after='log_transition')
        self.machine.add_transition('SYNACK', 'SYN_SENT', 'ESTABLISHED', after='log_transition')
        self.machine.add_transition('ACK', 'SYN_RCVD', 'ESTABLISHED', after='log_transition')
        self.machine.add_transition('CLOSE', 'LISTEN', 'CLOSED', after='log_transition')
        self.machine.add_transition('CLOSE', 'SYN_SENT', 'CLOSED', after='log_transition')
        self.machine.add_transition('CLOSE', 'SYN_RCVD', 'FIN_WAIT_1', after='log_transition')
        self.machine.add_transition('CLOSE', 'ESTABLISHED', 'FIN_WAIT_1', after='log_transition')
        self.machine.add_transition('FIN', 'ESTABLISHED', 'CLOSE_WAIT', after='log_transition')
        self.machine.add_transition('RDATA', 'ESTABLISHED', 'ESTABLISHED', after='on_data_received')
        self.machine.add_transition('SDATA', 'ESTABLISHED', 'ESTABLISHED', after='on_data_sent')
        self.machine.add_transition('ACK', 'FIN_WAIT_1', 'FIN_WAIT_2', after='log_transition')
        self.machine.add_transition('FIN', 'FIN_WAIT_1', 'CLOSING', after='log_transition')
        self.machine.add_transition('CLOSE', 'CLOSE_WAIT', 'LAST_ACK', after='log_transition')

    def log_transition(self, event_data):
        print(f"Event {event_data.event.name} received, current State is {self.state}")

    def on_data_received(self, event_data):
        self.data_count += 1
        print(f"DATA received {self.data_count}")

    def on_data_sent(self, event_data):
        self.data_count += 1
        print(f"DATA sent {self.data_count}")


def main():
    tcp = TCPFSM()
    for line in sys.stdin:
        for token in line.split():
            if token not in VALID_EVENTS:
                print(f"Error: unexpected Event: {token}")
                continue
            try:
                tcp.trigger(token)
            except (MachineError, AttributeError) as error:
                print(error)


if __name__ == '__main__':
    main()
