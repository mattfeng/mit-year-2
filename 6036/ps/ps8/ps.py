import numpy as np

class Module():
    pass

class ReLU(Module):
    """
    ReLU
    """

    def forward(self, Z, dropout_pct=0.):
        # Z is a column vector of pre-activations;
        # return A a column vector of activations
        keep_pct = 1 - dropout_pct
        mask = np.random.binomial(1, keep_pct, Z.shape)

        zero_out = np.where((mask == 0) |  (Z < 0))
        if keep_pct < 1e-10:
            raise Exception("Dropout percentage too high")
        self.A = Z / keep_pct
        self.A[zero_out] = 0

        return self.A

class Linear(Module):
    """
    Fully-connected layer
    """

    def __init__(self, m, n):
        """
        m ()
        W (m x n matrix): W.T@data
        """
        self.m, self.n = m, n         # (in size, out size)
        self.W0 = np.zeros(shape=[self.n, 1])  # (n x 1)
        self.W = np.random.normal(0, 1.0 * m ** (-.5), size=[m, n]) # (m x n)
        self.dLdW = None
        self.dLdW0 = None
        # Your initialization code for Adadelta here
        self.gamma = 0.9
        self.epsilon = 1e-8
        self.G = np.zeros_like(self.W)
        self.G0 = np.zeros_like(self.W0)

    def sgd_step(self, lrate):
        """
        Gradient descent step
        """
        # Assume that self.dldW and self.dLdW0 have been set by 'backward'
        # Your code for Adadelta here
        self.G = self.gamma * self.G + (1 - self.gamma) * self.dLdW ** 2
        self.G0 = self.gamma * self.G0 + (1 - self.gamma) * self.dLdW0 ** 2

        self.W -= lrate * self.dLdW / (np.sqrt(self.G) + self.epsilon)
        self.W0 -= lrate * self.dLdW0 / (np.sqrt(self.G0) + self.epsilon)
        


print(ReLU().forward(np.full(10, -1), dropout_pct=0.0))