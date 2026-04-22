import unittest
from transitions import MachineError

from tcp_fsm import TCPFSM, VALID_EVENTS

class TestTCPFSM(unittest.TestCase):
    def test_start_state_is_closed(self):
        fsm = TCPFSM()
        self.assertEqual(fsm.state, 'CLOSED')

    def test_passive_open(self):
        fsm = TCPFSM()
        fsm.trigger('PASSIVE')
        self.assertEqual(fsm.state, 'LISTEN')

    def test_active_then_synack(self):
        fsm = TCPFSM()
        fsm.trigger('ACTIVE')
        fsm.trigger('SYNACK')
        self.assertEqual(fsm.state, 'ESTABLISHED')

    def test_close_path_to_fin_wait_2(self):
        fsm = TCPFSM()
        fsm.trigger('PASSIVE')
        fsm.trigger('SYN')
        fsm.trigger('ACK')
        fsm.trigger('CLOSE')
        fsm.trigger('ACK')
        self.assertEqual(fsm.state, 'FIN_WAIT_2')

    def test_data_events_in_established(self):
        fsm = TCPFSM()
        fsm.trigger('PASSIVE')
        fsm.trigger('SYN')
        fsm.trigger('ACK')
        fsm.trigger('RDATA')
        fsm.trigger('SDATA')
        self.assertEqual(fsm.state, 'ESTABLISHED')
        self.assertEqual(fsm.data_count, 2)

    def test_invalid_transition_raises_error(self):
        fsm = TCPFSM()
        with self.assertRaises(MachineError):
            fsm.trigger('ACK')

    def test_valid_events_have_10_items(self):
        self.assertEqual(len(VALID_EVENTS), 10)


if __name__ == '__main__':
    unittest.main()
