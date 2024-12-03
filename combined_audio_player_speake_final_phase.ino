#include <WiFi.h>
#include <WiFiClient.h>
#include <SD.h>
#include "Arduino.h"

// WiFi credentials
const char* ssid = "esp8266";
const char* password = "9876543210";

// Static IP configuration
IPAddress staticIP(192, 168, 137, 100); // Desired static IP
IPAddress gateway(192, 168, 1, 1);      // Hotspot gateway (e.g., 192.168.1.1)
IPAddress subnet(255, 255, 255, 0);     // Subnet mask

// Server configuration
const int serverPort = 8080;
WiFiServer server(serverPort);

// SD card configuration
const int chipSelect = 5;
#define DAC_PIN 25 // DAC output pin for audio
#define NUM_BYTES_TO_READ_FROM_FILE 1024

// WAV Header Structure
struct WavHeader_Struct {
  char RIFFSectionID[4];      // "RIFF"
  uint32_t Size;              // File size - 8 bytes
  char RiffFormat[4];         // "WAVE"
  char FormatSectionID[4];    // "fmt"
  uint32_t FormatSize;        // Format section size
  uint16_t FormatID;          // 1 = PCM
  uint16_t NumChannels;       // Number of channels (1 = mono, 2 = stereo)
  uint32_t SampleRate;        // Sampling rate
  uint32_t ByteRate;          // Byte rate
  uint16_t BlockAlign;        // Block align
  uint16_t BitsPerSample;     // Bits per sample (e.g., 16)
  char DataSectionID[4];      // "data"
  uint32_t DataSize;          // Data section size
} WavHeader;

File WavFile;
bool IsMono = false;
const int blinkPin = 15;

void setup() {
  Serial.begin(115200);
  pinMode(blinkPin, HIGH);

  // Configure static IP
  WiFi.config(staticIP, gateway, subnet);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected!");

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Initialize SD card
  if (!SD.begin(chipSelect)) {
    Serial.println("SD card initialization failed!");
    while (1);
  }
  Serial.println("SD card initialized!");

  // Start server
  server.begin();
  Serial.println("Server started!");

}

void loop() {
  

  WiFiClient client = server.available();
  if (client) {
    Serial.println("Client connected!");
    digitalWrite(blinkPin, HIGH);


    // Receive filename
    String filename = client.readStringUntil('\n');
    filename.trim(); // Remove extra spaces or newline
    Serial.print("Receiving file: ");
    Serial.println(filename);

    // Open file on SD card
    File file = SD.open("/" + filename, FILE_WRITE);
    if (!file) {
      Serial.println("Failed to open file on SD card!");
      client.stop();
      return;
    }

    // Receive file data
    while (client.connected()) {
      while (client.available()) {
        uint8_t data = client.read();
        file.write(data);
      }
    }

    file.close();
    Serial.println("File saved to SD card!");
    client.stop();

    // Play the file after receiving
    if (PlayWav("/" + filename)) {
      Serial.println("Audio playback completed.");
    } else {
      Serial.println("Failed to play the audio file.");
    }
  }
}

bool PlayWav(const String& filename) {
  // Open WAV file
  WavFile = SD.open(filename.c_str());
  if (!WavFile) {
    Serial.println("Error: Could not open WAV file.");
    return false;
  }

  // Read and validate WAV header
  WavFile.read((byte*)&WavHeader, sizeof(WavHeader));
  // if (!ValidateWavHeader(&WavHeader)) {
  //   Serial.println("Invalid WAV file.");
  //   return false;
  // }

  IsMono = (WavHeader.NumChannels == 1);
  Serial.println("WAV file ready. Starting playback...");

  // Playback loop
  static uint8_t Samples[NUM_BYTES_TO_READ_FROM_FILE];
  while (true) {
    size_t BytesRead = WavFile.read(Samples, sizeof(Samples));

    // Check if end of file is reached
    if (BytesRead == 0) {
      WavFile.close();
      return true; // End of playback
    }

    // Playback the audio data
    for (size_t i = 0; i < BytesRead; i += (IsMono ? 2 : 4)) {
      int16_t Sample;

      // Read 16-bit sample (if stereo, pick one channel)
      if (IsMono) {
        Sample = (Samples[i + 1] << 8) | Samples[i]; // Mono
      } else {
        Sample = (Samples[i + 3] << 8) | Samples[i + 2]; // Right channel
      }

      // Convert 16-bit sample to 8-bit for DAC (0–255 range)
      uint8_t DacValue = map(Sample, -32768, 32767, 0, 255);

      // Output to DAC
      dacWrite(DAC_PIN, DacValue);
      digitalWrite(blinkPin, HIGH);

      // Delay to match sample rate
      delayMicroseconds(1000000 / WavHeader.SampleRate);
      digitalWrite(blinkPin, LOW);
      
    }
  }
}

bool ValidateWavHeader(WavHeader_Struct* Wav) {
  if (memcmp(Wav->RIFFSectionID, "RIFF", 4) != 0) return false;
  if (memcmp(Wav->RiffFormat, "WAVE", 4) != 0) return false;
  if (memcmp(Wav->FormatSectionID, "fmt", 3) != 0) return false;
  if (memcmp(Wav->DataSectionID, "data", 4) != 0) return false;
  if (Wav->FormatID != 1) return false; // PCM format
  if ((Wav->BitsPerSample != 16)) return false; // Only support 16-bit samples
  return true;
}
