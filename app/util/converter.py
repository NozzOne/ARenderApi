from time import time

from app.database.schemas import DefaultModel


async def convertStruct(source, status:bool, code:int, message:str)->DefaultModel:
    return {
        "status": status,
        "system": {
            "code": code,
            "message": message
        },
        "source": source,
        "timestemp": time()
    }

__all__ = ['convertStruct']