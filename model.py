# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = Modelfromdict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
import json

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class ModelElement:
    tokenName: str
    rank: int
    lowestDate18_19: str
    lowestPrice18_19: float
    lowestDate18_20: str
    lowestPrice18_20: float
    usdtPrice: float
    marketCap: float

    @staticmethod
    def from_dict(obj: Any) -> 'ModelElement':
        assert isinstance(obj, dict)
        tokenName = from_str(obj.get("tokenName"))
        rank = from_int(obj.get("rank"))
        lowestDate18_19 = from_str(obj.get("lowestDate_18_19"))
        lowestPrice18_19 = from_float(obj.get("lowestPrice_18_19"))
        lowestDate18_20 = from_str(obj.get("lowestDate_18_20"))
        lowestPrice18_20 = from_float(obj.get("lowestPrice_18_20"))
        usdtPrice = from_float(obj.get("usdtPrice"))
        marketCap = from_float(obj.get("marketCap"))
        return ModelElement(tokenName, rank, lowestDate18_19, lowestPrice18_19, lowestDate18_20, lowestPrice18_20, usdtPrice, marketCap)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tokenName"] = from_str(self.tokenName)
        result["rank"] = from_int(self.rank)
        result["lowestDate_18_19"] = from_str(self.lowestDate18_19)
        result["lowestPrice_18_19"] = to_float(self.lowestPrice18_19)
        result["lowestDate_18_20"] = from_str(self.lowestDate18_20)
        result["lowestPrice_18_20"] = to_float(self.lowestPrice18_20)
        result["usdtPrice"] = to_float(self.usdtPrice)
        result["marketCap"] = to_float(self.marketCap)
        return result


def Modelfromdict(s: Any) -> List[ModelElement]:
    return from_list(ModelElement.from_dict, s)


def Modeltodict(x: List[ModelElement]) -> Any:
    return from_list(lambda x: to_class(ModelElement, x), x)
