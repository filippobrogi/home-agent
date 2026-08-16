from enum import Enum

from pydantic import BaseModel


class TestStatus(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class LogAnalysis(BaseModel):
    status: TestStatus
    root_cause: str
    evidence: list[str]
    recommendation: str
    confidence: float
