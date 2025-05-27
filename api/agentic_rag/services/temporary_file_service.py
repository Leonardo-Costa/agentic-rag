from contextlib import asynccontextmanager
import os
import shutil
import tempfile
from typing import List

from fastapi import UploadFile


class TemporaryFileService:
    def __init__(self, temp_dir: str = None):
        self.temp_dir = temp_dir or os.getenv('TEMP_DIR', tempfile.gettempdir())
        os.makedirs(self.temp_dir, exist_ok=True)

    async def save_uploaded_file(self, file: UploadFile, path: str) -> None:
        try:
            with open(path, "wb") as buffer:
                await file.seek(0)
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise Exception(f"Failed to save file {file.filename}: {str(e)}")

    def cleanup_files(self, file_paths: List[str]) -> None:
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Warning: Could not remove temp file {file_path}: {e}")

    def cleanup_directory(self, dir_path: str) -> None:
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
        except Exception as e:
            print(f"Warning: Could not remove temp directory {dir_path}: {e}")

    @asynccontextmanager
    async def temp_file_context(self, upload_file: UploadFile):
        temp_dir = tempfile.mkdtemp(dir=self.temp_dir)
        temp_file_path = os.path.join(temp_dir, upload_file.filename)
        
        try:
            await self.save_uploaded_file(upload_file, temp_file_path)
            yield temp_file_path
        finally:
            self.cleanup_directory(temp_dir)

    @asynccontextmanager
    async def temp_batch_dir_context(self):
        batch_temp_dir = tempfile.mkdtemp(dir=self.temp_dir)
        try:
            yield batch_temp_dir
        finally:
            self.cleanup_directory(batch_temp_dir)