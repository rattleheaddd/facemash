import tensorflow as tf
import tf2onnx
import onnx

# 1. Load your best Keras model
print("Loading Keras model...")
model = tf.keras.models.load_model('best_resnet152_model.keras', compile=False)

# 2. Define the input signature matching your data shape (Batch size=1 for single image speed)
input_signature = [tf.TensorSpec([1, 224, 224, 3], tf.float32, name='input_image')]

# 3. Convert to ONNX format
print("Converting Keras graph to ONNX...")
onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature, opset=13)

# 4. Save the ONNX file to your laptop
onnx_filename = "resnet152_optimized.onnx"
onnx.save(onnx_model, onnx_filename)
print(f"✅ Success! Saved ONNX model as: {onnx_filename}")
