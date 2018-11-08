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
            raise Exception("Dropout too high")
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
        self.W0 = np.zeros(size=[self.n, 1])  # (n x 1)
        self.W = np.random.normal(0, 1.0 * m ** (-.5), size=[m, n]) # (m x n)
        # Your initialization code for Adadelta here

    def sgd_step(self, lrate):          # Gradient descent step
        # Assume that self.dldW and self.dLdW0 have been set by 'backward'
        # Your code for Adadelta here
        self.W -= lrate*self.dLdW
        self.W0 -= lrate*self.dLdW0


print(ReLU().forward(np.full(10, -1), dropout_pct=0.0))