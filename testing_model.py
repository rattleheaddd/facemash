import onnxruntime as ort
import numpy as np
import time


# 1. Initialize ONNX runtime session optimized for CPU execution
opts = ort.SessionOptions()
opts.intra_op_num_threads = 4  # Set to the number of physical cores on your laptop CPU
opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

session = ort.InferenceSession("resnet152_optimized.onnx", opts)

# Get the name of the input layer
input_name = session.get_inputs()[0].name

# 2. Generate dummy data for inference
dummy_input = np.random.rand(1, 224, 224, 3).astype(np.float32)

# 3. Warm up the engine
_ = session.run(None, {input_name: dummy_input})

# 4. Benchmark 10 loops
print("Benchmarking ONNX latency on CPU...")
start_time = time.time()
for _ in range(10):
    _ = session.run(None, {input_name: dummy_input})
end_time = time.time()

onnx_latency = (end_time - start_time) / 10
print("\n=====================================")
print(f"⏱️ ONNX CPU Speed: {onnx_latency * 1000:.2f} ms per image")
print("=====================================")
