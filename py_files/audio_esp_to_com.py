import socket
import os

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8080       # Port number (must match the ESP32 client)

# Directory to save the received audio files
SAVE_DIRECTORY = "C:/Users/SERGPC1/Desktop/Nexoai/py_files"  # Change to your desired directory
operation_done = False

# Ensure the directory exists
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

# List of allowed audio extensions
ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.aac', '.flac', '.ogg']

def is_audio_file(filename):
    """Check if the file has an audio file extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        
        # Receive the file name
        filename = conn.recv(1024).decode().strip()
        print(f"Receiving file: {filename}")
        
        if not is_audio_file(filename):
            print(f"Received file is not an audio file: {filename}")
            conn.close()
            return
        
        filepath = os.path.join(SAVE_DIRECTORY, filename)
        
        # Open the file for writing
        with open(filepath, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)

        print(f"File received and saved at {filepath}")
        
        # Verify if the file is a valid .wav file
        if filename.endswith('.wav'):
            try:
                with open(filepath, 'rb') as file:
                    file_header = file.read(4)
                    if file_header != b"RIFF":
                        print(f"Error: Not a valid WAV file: {filename}")
                    else:
                        print(f"File successfully received and verified as WAV.")
                        return True
            except Exception as e:
                print(f"Error verifying WAV file: {e}")
        
        conn.close()

if __name__ == "__main__":
    main()
