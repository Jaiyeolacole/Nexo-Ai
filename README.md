Nexo AI is a cutting-edge project that utilizes the ESP32 microcontroller to integrate I2S audio recording capabilities with the INMP411 microphone module. The project aims to record high-quality, distinct audio signals that can be further processed for various AI-driven applications such as speech recognition, sound classification, or environmental monitoring.

Features:
  ESP32 I2S Audio Integration: Leveraging the power of the ESP32's I2S interface for efficient audio data capture.
  High-Quality Audio Input: Compatible with the INMP411 microphone module for clear and accurate audio recordings.
  Open-Source: Fully open and customizable for developers to extend and adapt to their specific needs.

Procedure:
  Connect the INMP411 to the ESP32 pins as described in the hardware configuration section.
  Load the provided firmware onto the ESP32 using Arduino IDE or PlatformIO.
  
Capture Audio:
  Start recording audio by running the integrated sketch.
  Access the captured audio via the ESP32's storage or send it to a connected device for processing.

Deploy for AI Processing:
  Use the audio files with machine learning frameworks such as Edge Impulse, TensorFlow Lite, or custom AI models.
  Contributions are welcome! Feel free to open issues, submit pull requests, or suggest improvements to make Nexo AI even better.

  Thanks to https://github.com/0015/ThatProject/tree/master/ESP32_MICROPHONE/ESP32_INMP441_RECORDING for making this code open source, i modified it and make it suitable for my application.
