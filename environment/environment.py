from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
import numpy as np

from scipy.spatial import distance
from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

tf.compat.v1.enable_v2_behavior()

class VirtualEnv(py_environment.PyEnvironment):

  def __init__(self):
    #Action array with 4 elementa
    self._action_spec = array_spec.BoundedArraySpec(
        shape=(), dtype=np.int32, minimum=0, maximum=50, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(1,), dtype=np.int32, minimum=0, name='observation')
    self._state = 0
    self._local_step = 0
    self._episode_ended = False
    self._arrayMetrics = []
    lines = open('step.txt','r').read().split('\n')
    for line in lines:
        self._arrayMetrics.append(line)

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self._local_step = 0
    self._state = 0
    self._episode_ended = False
    return ts.restart(np.array([self._state], dtype=np.int32))

  def _step(self, action):

    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()

    if self._local_step == 200:
        self._episode_ended = True
    else:
        self._state += abs(int(self._arrayMetrics[self._local_step]) - action)          
        self._local_step += 1

    if self._episode_ended == True or self._state >= 50:
        reward = self._local_step
        self._episode_ended = True
        return ts.termination(np.array([self._state], dtype=np.int32), reward)
    else:
        reward = self._local_step
        return ts.transition(
            np.array([self._state], dtype=np.int32), reward=reward, discount=0.9)       


environment = VirtualEnv()
time_step = environment.reset()
print(time_step)

cumulative_reward = time_step.reward

time_step = environment.step(40)
time_step2 = environment.step(10)
time_step3 = environment.step(50)
time_step4 = environment.step(10)

time_step5 = environment.step(10)
print(time_step)
print(time_step2)
print(time_step3)
print(time_step4)
print(time_step5)