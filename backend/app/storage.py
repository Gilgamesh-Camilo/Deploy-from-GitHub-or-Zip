from fastapi import UploadFile
import aiofiles

async def save_file(upload_file: UploadFile, dest_path: str):
    async with aiofiles.open(dest_path, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)

async def load_file(path: str):
    async with aiofiles.open(path, 'rb') as f:
        return await f.read()
