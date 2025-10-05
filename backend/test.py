import os

file_path = 'backend/credentials.json'
print(os.path.abspath(file_path))
print(os.path.exists(file_path))
