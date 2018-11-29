import pdb
import random
import numpy as np
from dist import uniform_dist, delta_dist, mixture_dist
from util import argmax_with_val, argmax
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import Adam

class MDP:
    # Needs the following attributes:
    # states: list or set of states
    # actions: list or set of actions
    # discount_factor: real, greater than 0, less than or equal to 1
    # start: optional instance of DDist, specifying initial state dist
    #    if it's unspecified, we'll use a uniform over states
    # These are functions:
    # transition_model: function from (state, action) into DDist over next state
    # reward_fn: function from (state, action) to real-valued reward

    def __init__(self, states, actions, transition_model, reward_fn,
                     discount_factor = 1.0, start_dist = None):
        self.states = states
        self.actions = actions
        self.transition_model = transition_model
        self.reward_fn = reward_fn
        self.discount_factor = discount_factor
        self.start = start_dist if start_dist else uniform_dist(states)

    # Given a state, return True if the state should be considered to
    # be terminal.  You can think of a terminal state as generating an
    # infinite sequence of zero reward.
    def terminal(self, s):
        return False

    # Randomly choose a state from the initial state distribution
    def init_state(self):
        return self.start.draw()

    # Simulate a transition from state s, given action a.  Return
    # reward for (s,a) and new state, drawn from transition.  If a
    # terminal state is encountered, sample next state from initial
    # state distribution
    def sim_transition(self, s, a):
        return (self.reward_fn(s, a),
                self.init_state() if self.terminal(s) else
                    self.transition_model(s, a).draw())

# Perform value iteration on an MDP, also given an instance of a q
# function.  Terminate when the max-norm distance between two
# successive value function estimates is less than eps.
# interactive_fn is an optional function that takes the q function as
# argument; if it is not None, it will be called once per iteration,
# for visuzalization

# The q function is typically an instance of TabularQ, implemented as a
# dictionary mapping (s, a) pairs into Q values This must be
# initialized before interactive_fn is called the first time.

def value_iteration(mdp, q, eps=0.01, max_iters=1000):
    i = 0
    while i < max_iters:
        new_q = q.copy()
        
        for state in mdp.states:
            for action in mdp.actions:
                new_value = mdp.reward_fn(state, action) + \
                    mdp.discount_factor * sum(list(map(lambda i: i[1] * value(q, i[0]), mdp.transition_model(state, action).d.items())))
                new_q.set(state, action, new_value)
        
        diff = [] # check if we can terminate iteration (max delta < eps)
        for state in mdp.states:
            for action in mdp.actions:
                diff.append(abs(new_q.get(state, action) - q.get(state, action)))
        if max(diff) < eps:
            break
        
        i += 1
        q = new_q
        
    return new_q

# Given a state, return the value of that state, with respect to the
# current definition of the q function
def value(q, s):
    return max(map(lambda a: q.get(s, a), q.actions))

# Given a state, return the action that is greedy with reespect to the
# current definition of the q function
def greedy(q, s):
    return max(map(lambda a: (q.get(s, a), a), q.actions), key=lambda x: x[0])[1]

def epsilon_greedy(q, s, eps = 0.5):
    if random.random() < eps:  # True with prob eps, random action
        return uniform_dist(q.actions).draw()
    else:
        return greedy(q, s)


class TabularQ:
    def __init__(self, states, actions):
        self.actions = actions
        self.states = states
        self.q = dict([((s, a), 0.0) for s in states for a in actions])

    def copy(self):
        q_copy = TabularQ(self.states, self.actions)
        q_copy.q.update(self.q)
        return q_copy

    def set(self, s, a, v):
        self.q[(s,a)] = v

    def get(self, s, a):
        return self.q[(s,a)]

    def update(self, data, lr):
        for (s, a, t) in data:
            self.q[(s, a)] += lr * (t - self.q[(s, a)])

def Q_learn(mdp, q, lr=.1, iters=100, eps = 0.5, interactive_fn=None):
    s = mdp.init_state()

    for it in range(iters):
        if interactive_fn:
            interactive_fn(q, it)
        a = epsilon_greedy(q, s, eps)
        r, s_prime = mdp.sim_transition(s, a)
        maxq = value(q, s_prime)
        is_terminal = mdp.terminal(s)
        t = (0 if is_terminal else mdp.discount_factor * maxq) + r
        q.update([(s, a, t)], lr)
        s = s_prime

    return q

# Simulate an episode (sequence of transitions) of at most
# episode_length, using policy function to select actions.  If we find
# a terminal state, end the episode.  Return accumulated reward a list
# of (s, a, r, s') whee s' is None for transition from terminal state.
def sim_episode(mdp, episode_length, policy, draw=False):
    episode = []
    reward = 0
    s = mdp.init_state()
    for i in range(episode_length):
        a = policy(s)
        (r, s_prime) = mdp.sim_transition(s, a)
        reward += r
        if mdp.terminal(s):
            episode.append((s, a, r, None))
            return reward, episode
        episode.append((s, a, r, s_prime))
        if draw: mdp.draw_state(s)
        s = s_prime
    return reward, episode

# Return average reward for n_episodes of length episode_length
# while following policy (a function of state) to choose actions.
def evaluate(mdp, n_episodes, episode_length, policy):
    score = 0
    length = 0
    for i in range(n_episodes):
        # Accumulate the episode rewards
        r, e = sim_episode(mdp, episode_length, policy)
        score += r
        length += len(e)
        # print('    ', r, len(e))
    return 100, length / n_episodes
    # return score/n_episodes, length/n_episodes


def Q_learn_batch(mdp, q, lr=.1, iters=100, eps=0.5,
                  episode_length=10, n_episodes=2,
                  interactive_fn=None):
    experiences = []
    for it in range(iters):
        if interactive_fn:
            interactive_fn(q, it)

        for ep in range(n_episodes):
            policy = lambda s: epsilon_greedy(q, s, eps)
            ret, trajectory = sim_episode(mdp, episode_length, policy)
            experiences.append(trajectory)
        
        all_q_targets = []
        for exp in experiences:
            for (s, a, r, s_prime) in exp:
                t = r + (0 if s_prime is None else mdp.discount_factor * value(q, s_prime))
                q_target = (s, a, t)
                all_q_targets.append(q_target)
        
        q.update(all_q_targets, lr)

    return q


def make_nn(state_dim, num_hidden_layers, num_units):
    model = Sequential()
    model.add(Dense(num_units, input_dim = state_dim, activation='relu'))
    for i in range(num_hidden_layers-1):
        model.add(Dense(num_units, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer=Adam())
    return model


class NNQ:
    def __init__(self, states, actions, state2vec, num_layers, num_units, epochs=1):
        self.actions = actions
        self.states = states
        self.state2vec = state2vec
        self.epochs = epochs
        print("num states:", len(states))
        self.models = {
            a:make_nn(self.state2vec(states[0]).shape[1], num_layers, num_units) for a in actions
        }
        if self.models is None:
            raise NotImplementedError('NNQ.models')

    def get(self, s, a):
        return self.models[a].predict(self.state2vec(s))

    def update(self, data, lr):
        for action in self.actions:
            X = []
            Y = []
            for (s, a, t) in filter(lambda x: x[1] == action, data):
                X.append(self.state2vec(s).reshape(-1))
                Y.append(t)
            if len(X) == 0:
                continue
            X = np.array(X)
            Y = np.array(Y).reshape(-1, 1)
            self.models[action].fit(X, Y, epochs=self.epochs)
