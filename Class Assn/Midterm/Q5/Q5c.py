# !pip install gym[classic_control]
import gym
import pickle
import numpy as np

# Use saved model.
file = open('model.obj', 'rb')
model = pickle.load(file)
file.close()
q_table = model["q_table"]
bins = model["bins"]

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset()


# Transfer the continuous observation into the nearest matching discrete bin.
def Discrete(state, bins):
    index = []
    for i in range(len(state)):
        index.append(np.digitize(state[i], bins[i]) - 1)
    return tuple(index)


# Run an example of using cartpole model for 1000 steps.
current_state = Discrete(env.reset()[0], bins)
for _ in range(1000):
    current_state = Discrete(observation, bins)
    action = np.argmax(q_table[current_state])
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    if terminated or truncated:
        observation, info = env.reset()
env.close()
