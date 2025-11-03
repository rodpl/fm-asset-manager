"""Football Manager asset appender InvokeAI node extension."""

from .fm_kit_appender import FMKitAppenderInvocation, FMKitAppenderOutput
from .fm_logo_appender import FMLogoAppenderInvocation, FMLogoAppenderOutput
from .fm_portrait_appender import (
    FMPortraitAppenderInvocation,
    FMPortraitAppenderOutput,
)

__all__ = [
    "FMPortraitAppenderInvocation",
    "FMPortraitAppenderOutput",
    "FMLogoAppenderInvocation",
    "FMLogoAppenderOutput",
    "FMKitAppenderInvocation",
    "FMKitAppenderOutput",
]
