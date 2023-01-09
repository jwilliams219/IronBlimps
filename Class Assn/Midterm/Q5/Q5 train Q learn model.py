# based on
# https://medium.com/analytics-vidhya/q-learning-is-the-most-basic-form-of-reinforcement-learning-which-doesnt-take-advantage-of-any-8944e02570c5
# !pip install gym[classic_control]

import numpy as np
import gym
import matplotlib.pyplot as plt
import pickle

# Observation possibilities in range, actions
bin_size = 50
observations = 4

# Set up discrete observation space and a Q table.
bins = [np.linspace(-4.8, 4.8, bin_size),
        np.linspace(-4, 4, bin_size),
        np.linspace(-0.418, 0.418, bin_size),
        np.linspace(-4, 4, bin_size)]

q_table = np.random.uniform(low=-1, high=1, size=([bin_size] * observations + [2]))


# Transfer the continuous observation into the nearest matching discrete bin.
def Discrete(state, bins):
    index = []
    for i in range(len(state)):
        index.append(np.digitize(state[i], bins[i]) - 1)
    return tuple(index)


env = gym.make("CartPole-v1", render_mode="rgb_array")
print(env.action_space)


# Train the Q learning model for n episodes with parameters.
def Q_learning(q_table, bins, episodes=10000, gamma=0.99, learning_rate=0.15, timestep=100, epsilon=0.2):
    rewards = 0
    steps = 0
    for episode in range(1, episodes + 1):
        steps += 1

        current_state = Discrete(env.reset()[0], bins)  # Get the discrete observation.

        score = 0
        terminated = False
        truncated = False
        while not terminated or truncated:
            if episode % timestep == 0:
                # env.render()
                pass
            if np.random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[current_state])
            if terminated:  # Not sure why it occasionally terminates after choosing action,
                break  # but needed to prevent infinite loop.
            observation, reward, terminated, truncated, info = env.step(action)
            next_state = Discrete(observation, bins)
            score += reward

            if not terminated or truncated:  # Update the Q table
                max_future_q = np.max(q_table[next_state])
                current_q = q_table[current_state + (action,)]
                new_q = (1 - learning_rate) * current_q + learning_rate * (reward + gamma * max_future_q)
                q_table[current_state + (action,)] = new_q
            current_state = next_state

        else:
            rewards += score
            if score > 200 and steps >= 100:
                print('Solved Episode: ', episode)
        if episode % timestep == 0:
            print("reward:", reward, "time:", timestep, " : ", reward / timestep)


Q_learning(q_table, bins)

# Save current model to file.
model = {"q_table": q_table, "bins": bins}
file = open('model.obj', 'wb')
pickle.dump(model, file)
file.close()
