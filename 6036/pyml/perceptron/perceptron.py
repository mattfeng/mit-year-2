import numpy as np

def perceptron_origin(data, labels, params={}, hook=None):
    """
    :param data:    array of dimension d x n
    :param labels:  array of dimension 1 x n
    :param params:  extra parameters to this algorithm;
                    your algorithm should run a number of
                    iterations equal to T
    :param hook:    a function that takes the tuple (th, th0) as an
                    argument and displays the separator graphically.
    :type data:     numpy.array
    :type labels:   numpy.array
    :type params:   dictionary
    :return:        theta
    """
    T = params.get('T', 100) # if T not in params, default to 100
    d, n = data.shape
    th = np.zeros(shape=(d, 1))


    for _ in range(T):
        error = False
        for i in range(n):
            x, y = data[:, i, np.newaxis], labels[np.newaxis, :, i]
            if y * np.asscalar(np.matmul(th.T, x)) <= 0:
                error = True
                if hook:
                    hook(th)
                th += y * x
        if not error:
            break
    
    return th

def perceptron(data, labels, params={}, hook=None):
    """
    :param data:    array of dimension d x n
    :param labels:  array of dimension 1 x n
    :param params:  extra parameters to this algorithm;
                    your algorithm should run a number of
                    iterations equal to T
    :param hook:    a function that takes the tuple (th, th0) as an
                    argument and displays the separator graphically.
    :type data:     numpy.array
    :type labels:   numpy.array
    :type params:   dictionary
    :return:        A tuple of theta (a d x 1 array) and
                    theta_0 (a 1 by 1 array).
    """
    T = params.get('T', 100) # if T not in params, default to 100
    logger = params.get('logger', None)
    d, n = data.shape
    th = np.zeros(shape=(d, 1))
    th0 = np.zeros(shape=(1, 1))

    for it in range(T):
        for i in range(n):
            x, y = data[:, i, np.newaxis], labels[np.newaxis, :, i]
            if logger:
                logger(it, i, x, y, th, th0)

            if y * (np.matmul(th.T, x) + th0) <= 0:
                if hook:
                    hook(th, th0)
                th += y * x
                th0 += y
    
    return (th, th0)

def averaged_perceptron(data, labels, params={}, hook=None):
    """
    :param data:    array of dimension d x n
    :param labels:  array of dimension 1 x n
    :param params:  extra parameters to this algorithm;
                    your algorithm should run a number of
                    iterations equal to T
    :param hook:    a function that takes the tuple (th, th0) as an
                    argument and displays the separator graphically.
    :type data:     numpy.array
    :type labels:   numpy.array
    :type params:   dictionary
    :return:        A tuple of theta (a d x 1 array) and
                    theta_0 (a 1 by 1 array), which is the average
                    over all values that th0 and th took on throughout
                    the training process.
    """
    T = params.get('T', 100) # if T not in params, default to 100
    logger = params.get('logger', None)
    d, n = data.shape

    # averaged perceptron will find the average over all the values
    # of perceptron
    th_sum = np.zeros(shape=(d, 1))
    th0_sum = np.zeros(shape=(1, 1))

    th = np.zeros(shape=(d, 1))
    th0 = np.zeros(shape=(1, 1))

    for it in range(T):
        for i in range(n):
            x, y = data[:, i, np.newaxis], labels[np.newaxis, :, i]
            if logger:
                logger(it, i, x, y, th, th0)
            if y * (np.matmul(th.T, x) + th0) <= 0:
                if hook:
                    hook(th, th0)
                th += y * x
                th0 += y
            th_sum += th
            th0_sum += th0
    
    return (th_sum / (n * T), th0_sum / (n * T))

def eval_classifier(learner, data_train, labels_train, data_test, labels_test):
    th, th0 = learner(data_train, labels_train)
    num_correct = score(data_test, labels_test, th, th0)
    d_test, n_test = data_test.shape
    return np.asscalar(num_correct) / n_test

def eval_learning_alg(learner, data_gen, n_train, n_test, it):
    return sum(eval_classifier(learner, # evaluate the learning algo
                               *data_gen(n_train), # generate a train set
                               *data_gen(n_test)) # generate a test set
               for _ in range(it)) / it # compute the average

def xval_learning_alg(learner, data, labels, k):
    data_split = np.array_split(data, k, axis=1)
    labels_split = np.array_split(labels, k, axis=1)

    total_score = 0

    for test_ix in range(0, k):
        data_train = np.concatenate(data_split[:test_ix] +
            data_split[test_ix + 1:], axis=1)
        data_test = data_split[test_ix]

        labels_train = np.concatenate(labels_split[:test_ix] +
            labels_split[test_ix + 1:], axis=1) 
        labels_test = labels_split[test_ix]

        total_score += eval_classifier(learner, data_train, labels_train, data_test, labels_test)
    
    return total_score / k



if __name__ == "__main__":
    data = [[ 1, 0, -1.5],
            [-1, 1, -1.0]]
    labels = [[1, -1, 1]]
    data = np.array(data)
    labels = np.array(labels)
    print(perceptron(data, labels))

