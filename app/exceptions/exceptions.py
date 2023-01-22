from typing import Dict


class APIException(Exception):
    """
    Base API Exception

    Example:
    {
        "status":bool,
        "system":{
            "code":int,
            "message":str
        },
    "data":dict
    }
    """
    def __init__(self, status:bool, system:Dict[str, int], source:None):
        self.status = status
        self.system = system
        self.source = source
