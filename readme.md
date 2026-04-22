# Lab 6 Report: TCP FSM

Name: Qi, Songqiao
Date: April 22, 2026
NYU ID: sq2326
Course: CSCI-GA.2662-001 Data Comm Networks

Affirmation of my Independent Effort
Sign: QI SONGQIAO

## overview

This program simulates the TCP protocol as a finite state machine.
It reads TCP event strings from standard input, one or more per line, and moves through the TCP states.

Main entry point: tcp_fsm.py (main() function in tcp_fsm.py)

## library

The program is written in Python.
I have the `transitions` library, version 0.9.3, which is a FSM package. I used this instead of the Java package.

## Design

There are 11 states in the machine:
CLOSED, LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSING, CLOSE_WAIT, LAST_ACK, and TIME_WAIT.

These are input events:
PASSIVE, ACTIVE, SYN, SYNACK, ACK, RDATA, SDATA, FIN, CLOSE, and TIMEOUT.

The transitions from Figure 1 are implemented in the code. The only one left out is the LISTEN to SYN_SENT SEND transition, see Note 2.

There are 3 action callbacks in the TCP_FSM.

`log_transition` is used for most transitions. It prints something like:
Event <event> received, current State is <state>

`on_data_received` is used for RDATA when the machine is in ESTABLISHED. It prints:
DATA received <n>

`on_data_sent` is used for SDATA when the machine is in ESTABLISHED. It prints:
DATA sent <n>

The counter n stored as `data_count`. It increases for RDATA and SDATA events as required. 

## input handling

Valid event tokens send to the FSM with `tcp.trigger(token)`.
If unvalid event for the current state, `MachineError` printed.
If unvalid token, the program prints `Error: unexpected Event: <token>`.
The program exits at EOF.

## bash output

```text
$ echo "PASSIVE SYN ACK RDATA SDATA CLOSE ACK" | .venv/bin/python tcp_fsm.py
Event PASSIVE received, current State is LISTEN
Event SYN received, current State is SYN_RCVD
Event ACK received, current State is ESTABLISHED
DATA received 1
DATA sent 2
Event CLOSE received, current State is FIN_WAIT_1
Event ACK received, current State is FIN_WAIT_2
```

## test output
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.006s

OK
Event ACTIVE received, current State is SYN_SENT
Event SYNACK received, current State is ESTABLISHED
Event PASSIVE received, current State is LISTEN
Event SYN received, current State is SYN_RCVD
Event ACK received, current State is ESTABLISHED
Event CLOSE received, current State is FIN_WAIT_1
Event ACK received, current State is FIN_WAIT_2
Event PASSIVE received, current State is LISTEN
Event SYN received, current State is SYN_RCVD
Event ACK received, current State is ESTABLISHED
DATA received 1
DATA sent 2
Event PASSIVE received, current State is LISTEN
```

## citation

"generate simple unit test for tcp fsm", prompt, (GPT-5.3-Codex, April 22 version). https://chatgpt.com/