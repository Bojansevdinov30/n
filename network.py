import numpy as np
import pathlib
import matplotlib.pyplot as plt
​
def get_mnist():
    with np.load(f"{pathlib.Path('/workspaces/n/mnist.npz').absolute()}") as f:
        images, labels = f["x_train"], f["y_train"]
    images = images.astype("float32") / 255
    images = np.reshape(images, (images.shape[0], images.shape[1] * images.shape[2]))
    labels = np.eye(10)[labels]
    return images, labels
​
images, labels = get_mnist()
w_i_h = np.random.uniform(-0.5, 0.5, (20, 784))
w_h_o = np.random.uniform(-0.5, 0.5, (10, 20))
b_i_h = np.zeros((20, 1))
b_h_o = np.zeros((10, 1))
​
learn_rate = 0.01
nr_correct = 0
epochs = 3
for epoch in range(epochs):
    for img, l in zip(images, labels):
        img = img.reshape(784, 1)
        l = l.reshape(10, 1)
        # Forward propagation input -> hidden
        h_pre = b_i_h + w_i_h @ img
        h = 1 / (1 + np.exp(-h_pre))
        # Forward propagation hidden -> output
        o_pre = b_h_o + w_h_o @ h
        o = 1 / (1 + np.exp(-o_pre))
​
        # Cost / Error calculation
        e = np.mean((o - l) ** 2)
        nr_correct += int(np.argmax(o) == np.argmax(l))
​
        # Backpropagation output -> hidden (cost function derivative)
        delta_o = o - l
        w_h_o += -learn_rate * delta_o @ np.transpose(h)
        b_h_o += -learn_rate * delta_o
        # Backpropagation hidden -> input (activation function derivative)
        delta_h = np.transpose(w_h_o) @ delta_o * (h * (1 - h))
        w_i_h += -learn_rate * delta_h @ np.transpose(img)
        b_i_h += -learn_rate * delta_h
​
    # Show accuracy for this epoch
    print(f"Acc: {round((nr_correct / images.shape[0]) * 100, 2)}%")
    nr_correct = 0
​
# Show results
while True:
    index = int(input("Vnesi broj (0 - 59999): "))
    if index < 0 or index >= images.shape[0]:
        print("Nevaliden indeks. Vnesi indeks pomegu 0 i 59999.")
        continue
    img = images[index]
    plt.imshow(img.reshape(28, 28), cmap="Greys")
​
    img = img.reshape(784, 1)
    # Forward propagation input -> hidden
    h_pre = b_i_h + w_i_h @ img
    h = 1 / (1 + np.exp(-h_pre))
    # Forward propagation hidden -> output
    o_pre = b_h_o + w_h_o @ h
    o = 1 / (1 + np.exp(-o_pre))
​
    plt.title(f"Ova e brojot {o.argmax()} ")
    plt.show()
​
