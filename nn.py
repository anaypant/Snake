import numpy as np

MODEL = [18, 12, 8, 4]  # Input, two hidden layers, output


class SnakeNN:
    def __init__(self):
        self.weights = [
            np.random.randn(MODEL[i], MODEL[i + 1]) * np.sqrt(2 / MODEL[i])
            for i in range(len(MODEL) - 1)
        ]

    def relu(self, x):
        return np.maximum(x, 0)
    def softmax(self, x):
        exps = np.exp(x - np.max(x))
        return exps / np.sum(exps)
    def tanh(self, x):
        return np.tanh(x)
    
    def forward(self, inp):
        assert len(inp) == MODEL[0], "Input size mismatch"
        layer_output = inp
        for weight in self.weights[:-1]:
            layer_output = self.tanh(np.dot(layer_output, weight))
        self.outputs = self.softmax(np.dot(layer_output, self.weights[-1]))
        self.key = np.argmax(self.outputs)

    def mutate(self, mutation_rate=0.2, mutation_strength=0.2):
        for i in range(len(self.weights)):
            mutation_mask = np.random.rand(*self.weights[i].shape) < mutation_rate
            noise = np.random.normal(0, mutation_strength, self.weights[i].shape)
            self.weights[i] += mutation_mask * noise

    def crossover(self, other):
        child = SnakeNN()
        for i in range(len(self.weights)):
            mask = np.random.rand(*self.weights[i].shape) < 0.5
            child.weights[i] = np.where(mask, self.weights[i], other.weights[i])
        return child
