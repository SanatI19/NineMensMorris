import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from collections import deque

class DQNAgent:
    def __init__(self, state_size, action_size, name="Agent"):
        self.state_size = state_size
        self.action_size = action_size
        self.name = name
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.memory = deque(maxlen=5000)
        self.model = self._build_model()

    def _build_model(self):
        """Define a deep Q-network"""
        model = Sequential([
            Dense(128, activation="relu", input_shape=(self.state_size,)),
            Dense(128, activation="relu"),
            Dense(self.action_size, activation="linear")  # One Q-value per action
        ])
        model.compile(loss="mse", optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def act(self, state, valid_actions):
        """Choose an action using epsilon-greedy strategy, considering only valid actions."""
        if np.random.rand() < self.epsilon:
            return random.choice(valid_actions)  # Random valid action (exploration)

        q_values = self.model.predict(np.array([state]), verbose=0)[0]

        # Mask invalid actions by setting their Q-values to -inf
        masked_q_values = np.full_like(q_values, -np.inf)
        masked_q_values[valid_actions] = q_values[valid_actions]

        return np.argmax(masked_q_values)  # Choose best valid action

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size=32):
        """Train using experience replay."""
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target += self.gamma * np.max(self.model.predict(np.array([next_state]), verbose=0))

            q_values = self.model.predict(np.array([state]), verbose=0)
            q_values[0][action] = target  # Update Q-value

            self.model.fit(np.array([state]), q_values, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
