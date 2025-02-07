from typing import List
from typing import Any
from dataclasses import dataclass
import json


@dataclass
class Result:
    date: str
    datatype: str
    station: str
    attributes: str
    value: float

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        _date = str(obj.get("date"))
        _datatype = str(obj.get("datatype"))
        _station = str(obj.get("station"))
        _attributes = str(obj.get("attributes"))
        _value = float(obj.get("value"))
        return Result(_date, _datatype, _station, _attributes, _value)

@dataclass
class Resultset:
    offset: int
    count: int
    limit: int

    @staticmethod
    def from_dict(obj: Any) -> 'Resultset':
        _offset = int(obj.get("offset"))
        _count = int(obj.get("count"))
        _limit = int(obj.get("limit"))
        return Resultset(_offset, _count, _limit)

@dataclass
class Metadata:
    resultset: Resultset

    @staticmethod
    def from_dict(obj: Any) -> 'Metadata':
        _resultset = Resultset.from_dict(obj.get("resultset"))
        return Metadata(_resultset)
@dataclass
class Root:
    metadata: Metadata
    results: List[Result]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _metadata = Metadata.from_dict(obj.get("metadata"))
        _results = [Result.from_dict(y) for y in obj.get("results")]
        return Root(_metadata, _results)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
