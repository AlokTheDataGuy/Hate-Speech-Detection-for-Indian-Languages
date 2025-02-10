import matplotlib.pyplot as plt

# Sample history data
# Replace these with actual lists from your model training history
epochs = range(1, len(training_accuracy) + 1)
training_accuracy = [0.76, 0.82, 0.85, 0.87]  # Example values
validation_accuracy = [0.74, 0.81, 0.83, 0.85]
training_loss = [0.45, 0.35, 0.28, 0.25]
validation_loss = [0.47, 0.37, 0.32, 0.29]

# Plotting Accuracy and Loss
plt.figure(figsize=(12, 6))

# Plot accuracy
plt.subplot(1, 2, 1)
plt.plot(epochs, training_accuracy, 'b-', label='Training Accuracy')
plt.plot(epochs, validation_accuracy, 'r-', label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Model Accuracy Over Epochs')
plt.legend()

# Plot loss
plt.subplot(1, 2, 2)
plt.plot(epochs, training_loss, 'b-', label='Training Loss')
plt.plot(epochs, validation_loss, 'r-', label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Model Loss Over Epochs')
plt.legend()

plt.tight_layout()
plt.savefig('model_performance_over_epochs.png')
plt.show()
