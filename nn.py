import numpy as np

MODEL = [32, 20, 12, 4]


class snake_nn:
    def __init__(self):
        self.weights = []
        for i in range(len(MODEL) - 1):
            a = MODEL[i]
            b = MODEL[i + 1]
            self.weights.append(2 * np.random.random((a, b)) - 1)

    def relu(self, x):
        return np.maximum(0, x)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def softmax(self, x):
        exp = np.exp(x - x.max())
        return exp / exp.sum()

    def tanh(self, x):
        return np.tanh(x)

    def forward(self, inp):
        self.hidden = []
        assert len(inp) == MODEL[0]
        self.hidden.append(self.tanh(np.dot(inp, self.weights[0])))
        self.hidden.append(self.tanh(np.dot(self.hidden[0], self.weights[1])))
        self.outputs = self.softmax(np.dot(self.hidden[1], self.weights[2]))

        self.key = np.argmax(self.outputs)
