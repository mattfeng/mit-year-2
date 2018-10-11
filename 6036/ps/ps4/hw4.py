import numpy as np
import scipy as np
import pandas as pd
import matplotlib.pyplot as plt

def rv(value_list):
    return np.array([value_list])

def cv(value_list):
    return np.transpose(rv(value_list))

def f1(x):
    return float((2 * x + 3)**2)

def df1(x):
    return 2 * 2 * (2 * x + 3)

def f2(v):
    x = float(v[0]); y = float(v[1])
    return (x - 2.) * (x - 3.) * (x + 3.) * (x + 1.) + (x + y -1)**2

def df2(v):
    x = float(v[0]); y = float(v[1])
    return cv([(-3. + x) * (-2. + x) * (1. + x) + \
               (-3. + x) * (-2. + x) * (3. + x) + \
               (-3. + x) * (1. + x) * (3. + x) + \
               (-2. + x) * (1. + x) * (3. + x) + \
               2 * (-1. + x + y), 
               2 * (-1. + x + y)])



def gd(f, df, x0, step_size_fn, max_iter):
    """
    :f: a function whose input is x, a column vector,
        and returns a scalar.
    :df: a function whose input is x, a column vector,
        and returns a column vector representing the
        gradient of f at x.
    :x0: an initial value of x, a column vector.
    :step_size_fn: a function that is given the iteration
        index (an integer) and returns a step size.
    :max_iter: the number of iterations to perform
    """
    fs = []
    xs = []
    x = x0
    for i in range(max_iter):
        eta = step_size_fn(i)
        fx = f(x)
        fs.append(fx)
        xs.append(np.copy(x))
        x -= eta * df(x)
    return x, fs, xs

def num_grad(f, delta=0.001):
    def df(x):
        x = x.reshape(-1)
        grad = []
        for ix, i in enumerate(x):
            shifted_x_plus = np.copy(x)
            shifted_x_plus[ix] = i + delta
            shifted_x_plus = cv(shifted_x_plus)

            shifted_x_minus = np.copy(x)
            shifted_x_minus[ix] = i - delta
            shifted_x_minus = cv(shifted_x_minus)

            grad.append((f(shifted_x_plus) - f(shifted_x_minus)) / (2 * delta))
        grad = np.array(grad).reshape(-1, 1)
        return grad

    return df

def minimize(f, x0, step_size_fn, max_iter):
    df = num_grad(f)
    return gd(f, df, x0, step_size_fn, max_iter)

def hinge(v):
    return np.maximum(0, 1 - v)

def hinge_loss(x, y, th, th0):
    """
    :x:   (d x n)
    :y:   (1 x n)
    :th:  (d x 1)
    :th0: (1 x 1)
    """
    margins = y * (np.matmul(th.T, x) + th0)
    return hinge(margins)

def svm_obj(x, y, th, th0, lam):
    """
    :x:
    :y:
    :th:
    :th0:
    """
    regularization = np.asscalar(lam * np.matmul(th.T, th))
    mean = np.asscalar(np.mean(hinge_loss(x, y, th, th0)))
    return mean + regularization

# Returns the gradient of hinge(v) with respect to v.
def d_hinge(v):
    return np.where(v >= 1, 0, -1)

# Returns the gradient of hinge_loss(x, y, th, th_0) with respect to th
def d_hinge_loss_th(x, y, th, th0):
    return x * y * d_hinge(y * (np.matmul(th.T, x) + th0))

# Returns the gradient of hinge_loss(x, y, th, th_0) with respect to th0
def d_hinge_loss_th0(x, y, th, th0):
    return y * d_hinge(y * (np.matmul(th.T, x) + th0))

# Returns the gradient of svm_obj(x, y, th, th_0) with respect to th
def d_svm_obj_th(x, y, th, th0, lam):
    reg = 2 * lam * th
    mean = np.mean(d_hinge_loss_th(x, y, th, th0), axis=1, keepdims=True)
    return mean + reg

# Returns the gradient of svm_obj(x, y, th, th_0) with respect to th0
def d_svm_obj_th0(x, y, th, th0, lam):
    return np.mean(d_hinge_loss_th0(x, y, th, th0), axis=1, keepdims=True)

# Returns the full gradient as a single vector
def svm_obj_grad(X, y, th, th0, lam):
    d_th = d_svm_obj_th(X, y, th, th0, lam)
    d_th0 = d_svm_obj_th0(X, y, th, th0, lam)
    return np.vstack([d_th, d_th0])

def batch_svm_min(data, labels, lam):
    def svm_min_step_size_fn(i):
       return 2 / (i+1) ** 0.5

    d, n = data.shape
    th = np.zeros((d, 1))
    th0 = np.zeros((1, 1))
    x0 = np.vstack([th, th0])
    print("x0", x0)
    J = lambda theta: svm_obj(data, labels, theta[:-1, :], theta[-1, :], lam)
    dJ = lambda theta: svm_obj_grad(data, labels, theta[:-1, :], theta[-1, :], lam)
    return gd(J, dJ, x0, svm_min_step_size_fn, 10)


def super_simple_separable():
    X = np.array([[2, 3, 9, 12],
                  [5, 2, 6, 5]])
    y = np.array([[1, -1, 1, -1]])
    return X, y

x_1, y_1 = super_simple_separable()
ans = batch_svm_min(x_1, y_1, 0.0001)