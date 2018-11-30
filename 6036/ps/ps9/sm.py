import numpy as np
class SM:
    start_state = None  # default start state

    def transition_fn(self, s, i):
        """
        Args:
            s: the current state
            i: the given input
        Returns:
            s': the next state
        """
        raise NotImplementedError

    def output_fn(self, s):
        """
        s:       the current state
        returns: the corresponding output
        """
        raise NotImplementedError
    
    def transduce(self, input_seq):
        """
        Transition, then output.
        """
        current_state = self.start_state
        transduced = []
        for action in input_seq:
            current_state = self.transition_fn(current_state, action)
            out = self.output_fn(current_state)
            transduced.append(out)
        return transduced


class Accumulator(SM):
    start_state = 0

    def transition_fn(self, s, i):
        return s + i

    def output_fn(self, s):
        return s


class Binary_Addition(SM):
    start_state = [0]

    def transition_fn(self, s, i):
        """
        State `s` contains the entire summed sequence.
        """
        sum_ = sum(i) + s[-1]
        if sum_ == 0:
            s[-1] = 0
            s.append(0)
        elif sum_ == 1:
            s[-1] = 1
            s.append(0)
        elif sum_ == 2:
            s[-1] = 0
            s.append(1)
        elif sum_ == 3:
            s[-1] = 1
            s.append(1)
            
        return s
    
    def output_fn(self, s):
        return s[-2]


class Reverser(SM):
    class ReverseState(object):
        def __init__(self):
            self.seq = []
            self.output_ix = None

    start_state = ReverseState()

    def transition_fn(self, s, i):
        if i == "end":
            s.output_ix = 0
        elif s.output_ix is not None:
            s.output_ix += 1
        else:
            s.seq = [i] + s.seq

        return s

    def output_fn(self, s):
        if s.output_ix is None or s.output_ix >= len(s.seq):
            return None
        return s.seq[s.output_ix]

        
class RNN(SM):
    def __init__(self, Wsx, Wss, Wo, Wss_0, Wo_0, f1, f2):
        self.start_state = np.zeros_like(Wss_0)
        self.Wsx = Wsx
        self.Wss = Wss
        self.Wss_0 = Wss_0
        self.Wo = Wo
        self.Wo_0 = Wo_0
        self.f1 = f1
        self.f2 = f2

    def transition_fn(self, s, i):
        """
        s (m x 1): Current state
        i (l x 1): Input

        """
        s = self.f1(self.Wsx@i + self.Wss@s + self.Wss_0)
        return s
        
    def output_fn(self, s):
        o = self.f2(self.Wo@s + self.Wo_0)
        return o
