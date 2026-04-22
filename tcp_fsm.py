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

        # Initial skeleton: establish path only; close/data handling comes later.
        self.machine.add_transition('PASSIVE', 'CLOSED', 'LISTEN', after='log_transition')
        self.machine.add_transition('ACTIVE', 'CLOSED', 'SYN_SENT', after='log_transition')
        self.machine.add_transition('SYN', 'LISTEN', 'SYN_RCVD', after='log_transition')
        self.machine.add_transition('SYN', 'SYN_SENT', 'SYN_RCVD', after='log_transition')
        self.machine.add_transition('SYNACK', 'SYN_SENT', 'ESTABLISHED', after='log_transition')
        self.machine.add_transition('ACK', 'SYN_RCVD', 'ESTABLISHED', after='log_transition')

    def log_transition(self, event_data):
        print(f"Event {event_data.event.name} received, current State is {self.state}")


def main():
    tcp = TCPFSM()
    for line in sys.stdin:
        for token in line.split():
            if token not in VALID_EVENTS:
                print(f"Error: unexpected Event: {token}")
                continue
            try:
                tcp.trigger(token)
            except MachineError as e:
                print(e)


if __name__ == '__main__':
    main()
