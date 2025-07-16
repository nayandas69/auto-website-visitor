#!/usr/bin/env python3

"""Scheduler functionality for Auto Website Visitor."""

import time
import threading
from typing import Callable, Optional
from datetime import datetime, timedelta
import schedule
from croniter import croniter

from .logger import VisitorLogger


class SchedulerManager:
    """Manages scheduled execution of website visits."""

    def __init__(self, logger: VisitorLogger):
        """Initialize scheduler manager.

        Args:
            logger: Logger instance
        """
        self.logger = logger
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

    def schedule_job(
        self, job_func: Callable, schedule_type: str, schedule_value: str
    ) -> None:
        """Schedule a job for execution.

        Args:
            job_func: Function to execute
            schedule_type: Type of schedule ('interval' or 'cron')
            schedule_value: Schedule value (e.g., '1h', '*/30 * * * *')
        """
        if schedule_type == "interval":
            self._schedule_interval(job_func, schedule_value)
        elif schedule_type == "cron":
            self._schedule_cron(job_func, schedule_value)
        else:
            raise ValueError(f"Unsupported schedule type: {schedule_type}")

    def _schedule_interval(self, job_func: Callable, interval_str: str) -> None:
        """Schedule job with interval.

        Args:
            job_func: Function to execute
            interval_str: Interval string (e.g., '1h', '30m', '45s')
        """
        interval_seconds = self._parse_interval(interval_str)

        def interval_job():
            while not self.stop_event.is_set():
                try:
                    self.logger.info(
                        f"Executing scheduled job (interval: {interval_str})"
                    )
                    job_func()
                    self.logger.info(
                        f"Scheduled job completed, next run in {interval_str}"
                    )
                except Exception as e:
                    self.logger.error(f"Scheduled job failed: {e}")

                # Wait for the interval or until stop event
                self.stop_event.wait(interval_seconds)

        self.thread = threading.Thread(target=interval_job, daemon=True)
        self.thread.start()
        self.running = True
        self.logger.info(f"Scheduled job with interval: {interval_str}")

    def _schedule_cron(self, job_func: Callable, cron_expr: str) -> None:
        """Schedule job with cron expression.

        Args:
            job_func: Function to execute
            cron_expr: Cron expression (e.g., '*/30 * * * *')
        """
        try:
            cron = croniter(cron_expr, datetime.now())
        except Exception as e:
            raise ValueError(f"Invalid cron expression '{cron_expr}': {e}")

        def cron_job():
            while not self.stop_event.is_set():
                try:
                    next_run = cron.get_next(datetime)
                    wait_seconds = (next_run - datetime.now()).total_seconds()

                    if wait_seconds > 0:
                        self.logger.info(
                            f"Next scheduled run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}"
                        )

                        # Wait until next run time or stop event
                        if self.stop_event.wait(wait_seconds):
                            break

                    if not self.stop_event.is_set():
                        self.logger.info(f"Executing scheduled job (cron: {cron_expr})")
                        job_func()
                        self.logger.info("Scheduled job completed")

                except Exception as e:
                    self.logger.error(f"Scheduled job failed: {e}")

        self.thread = threading.Thread(target=cron_job, daemon=True)
        self.thread.start()
        self.running = True
        self.logger.info(f"Scheduled job with cron expression: {cron_expr}")

    def _parse_interval(self, interval_str: str) -> int:
        """Parse interval string to seconds.

        Args:
            interval_str: Interval string (e.g., '1h', '30m', '45s')

        Returns:
            Interval in seconds

        Raises:
            ValueError: If interval format is invalid
        """
        interval_str = interval_str.lower().strip()

        if interval_str.endswith("s"):
            return int(interval_str[:-1])
        elif interval_str.endswith("m"):
            return int(interval_str[:-1]) * 60
        elif interval_str.endswith("h"):
            return int(interval_str[:-1]) * 3600
        elif interval_str.endswith("d"):
            return int(interval_str[:-1]) * 86400
        else:
            # Assume seconds if no unit specified
            try:
                return int(interval_str)
            except ValueError:
                raise ValueError(f"Invalid interval format: {interval_str}")

    def start(self) -> None:
        """Start the scheduler."""
        if not self.running:
            self.logger.info("Starting scheduler")
            self.running = True

    def stop(self) -> None:
        """Stop the scheduler."""
        if self.running:
            self.logger.info("Stopping scheduler")
            self.stop_event.set()
            self.running = False

            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=5)

    def is_running(self) -> bool:
        """Check if scheduler is running.

        Returns:
            True if scheduler is running, False otherwise
        """
        return self.running

    def wait_for_completion(self) -> None:
        """Wait for scheduler to complete (blocking)."""
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Scheduler interrupted by user")
            self.stop()
