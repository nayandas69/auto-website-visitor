#!/usr/bin/env python3

"""Auto Website Visitor - Automated website visiting with advanced features."""

__version__ = "3.0.0"
__author__ = "nayandas69"
__email__ = "nayanchandradas@hotmail.com"

from .core import AutoWebsiteVisitor
from .config import Config, VisitorSettings
from .scheduler import SchedulerManager
from .logger import setup_logger

__all__ = [
    "AutoWebsiteVisitor",
    "Config",
    "VisitorSettings",
    "SchedulerManager",
    "setup_logger",
]
