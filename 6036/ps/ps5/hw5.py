import numpy as np
# In all the following definitions:
# x is d by n : input data
# y is 1 by n : output regression values
# th is d by 1 : weights
# th0 is 1 by 1 or scalar

def lin_reg(x, th, th0):
    return np.matmul(th.T, x) + th0

def square_loss(x, y, th, th0):
    return (y - lin_reg(x, th, th0)) ** 2

def mean_square_loss(x, y, th, th0):
    return np.mean(square_loss(x, y, th, th0), axis=1, keepdims=True)

def d_lin_reg_th(x, th, th0):
    """
    Returns the gradient of lin_reg(x, th, th0) w.r.t. th.
    """
    return x
    
def d_square_loss_th(x, y, th, th0):
    """
    Returns the gradient of square_loss(x, y, th, th0) wrt th.
    """
    return 2 * (y - lin_reg(x, th, th0)) * -d_lin_reg_th(x, th, th0)

def d_mean_square_loss_th(x, y, th, th0):
    """
    Returns the gradient of mean_square_loss(x, y, th, th0) wrt th.
    """
    return np.mean(d_square_loss_th(x, y, th, th0), axis=1, keepdims=True)

def d_lin_reg_th0(x, th, th0):
    """
    Returns the gradient of lin_reg(x, th, th0) wrt th0.
    """
    d, n = x.shape
    return np.ones((1, n))
    
def d_square_loss_th0(x, y, th, th0):
    """
    Returns the gradient of square_loss(x, y, th, th0) wrt th0.
    """
    return 2 * (y - lin_reg(x, th, th0)) * -d_lin_reg_th0(x, th, th0)

# Write a function that returns the gradient of mean_square_loss(x, y, th, th0) with
# respect to th0.  It should be a one-line expression that uses d_square_loss_th0.
def d_mean_square_loss_th0(x, y, th, th0):
    return np.mean(d_square_loss_th0(x, y, th, th0), axis=1, keepdims=True)

def ridge_obj(x, y, th, th0, lam):
    return np.mean(square_loss(x, y, th, th0), axis=1, keepdims=True) + \
           lam * np.linalg.norm(th) ** 2

def d_ridge_obj_th(x, y, th, th0, lam):
    return d_mean_square_loss_th(x, y, th, th0) + 2 * lam * th

def d_ridge_obj_th0(x, y, th, th0, lam):
    return d_mean_square_loss_th0(x, y, th, th0)

def sgd(X, y, J, dJ, w0, step_size_fn, max_iter):
    d, n = X.shape
    w = w0
    fs = []
    ws = []
    for k in range(max_iter):           # k is the iteration (from Bellman)
        eta = step_size_fn(k)           # eta is the learning rate
        i = np.random.randint(n)        # randomly sample from dataset
        xi = X[:, i].reshape((-1, 1))   # get the sample
        yi = y[:, i].reshape((-1, 1))   # get the label
        f = J(xi, yi, w)                # compute cost
        grad = dJ(xi, yi, w)            # compute gradient

        ws.append(w.copy())             # store log
        fs.append(f)                

        w -= eta * grad                 # update weights
    
    return w, fs, ws
