import typing as t
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

    from pandas import Series as _PdSeries
    from pandas import DataFrame as PdDataFrame
    from pyarrow.plasma import ObjectID
    from pyarrow.plasma import PlasmaClient

    PdSeries = _PdSeries[t.Any]
    DataFrameOrient = Literal["split", "records", "index", "columns", "values", "table"]
    SeriesOrient = Literal["split", "records", "index", "table"]

    # numpy is always required by bentoml
    from numpy import generic as NpGeneric
    from numpy.typing import NDArray as _NDArray
    from numpy.typing import DTypeLike as NpDTypeLike  # type: ignore (incomplete numpy types)

    NpNDArray = _NDArray[t.Any]

    from xgboost import DMatrix

    from .starlette import ASGIApp
    from .starlette import ASGISend
    from .starlette import ASGIScope
    from .starlette import ASGIMessage
    from .starlette import ASGIReceive
    from .starlette import AsgiMiddleware

    __all__ = [
        "PdSeries",
        "PdDataFrame",
        "DataFrameOrient",
        "SeriesOrient",
        "ObjectID",
        "PlasmaClient",
        # xgboost
        "DMatrix",
        # numpy
        "NpNDArray",
        "NpGeneric",
        "NpDTypeLike",
        # starlette
        "AsgiMiddleware",
        "ASGIApp",
        "ASGIScope",
        "ASGISend",
        "ASGIReceive",
        "ASGIMessage",
    ]
