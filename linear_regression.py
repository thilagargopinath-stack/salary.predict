class LinearRegression:

    def __init__(self, x, y, alpha=0.0001, b0=0, b1=0):

        if len(x) != len(y):
            raise TypeError("x and y should have same number of rows.")

        self.x = x
        self.y = y
        self.alpha = alpha
        self.b0 = b0
        self.b1 = b1

    def predict(self, x):
        return self.b0 + self.b1 * x

    def error(self):
        return sum(
            (self.predict(xi) - yi) ** 2
            for xi, yi in zip(self.x, self.y)
        ) / len(self.x)

    def rmse(self):
        return self.error() ** 0.5

    def gradient(self, i):

        if i == 1:
            return sum(
                2 * (self.predict(xi) - yi) * xi
                for xi, yi in zip(self.x, self.y)
            ) / len(self.x)

        else:
            return sum(
                2 * (self.predict(xi) - yi)
                for xi, yi in zip(self.x, self.y)
            ) / len(self.x)

    def update(self, i):

        grad = self.gradient(i)

        if i == 1:
            self.b1 -= self.alpha * grad
        else:
            self.b0 -= self.alpha * grad

    def stop(self, epoch=1000):

        self.i += 1
        return self.i >= epoch

    def fit(self):

        self.i = 0

        while not self.stop():

            self.update(0)
            self.update(1)