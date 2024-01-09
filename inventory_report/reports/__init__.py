from typing import Dict, Type

from .complete_report import CompleteReport  # noqa:F401
from .report import Report  # noqa:F401
from .simple_report import SimpleReport  # noqa:F401

REPORTS: Dict[str, Type[Report]] = {
    "simple": SimpleReport,
    "complete": CompleteReport,
}
__all__ = ["CompleteReport", "Report", "SimpleReport", "REPORTS"]
