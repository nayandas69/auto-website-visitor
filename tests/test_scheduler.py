#!/usr/bin/env python3

"""Tests for scheduler functionality."""

import pytest
import time
import threading
from unittest.mock import Mock, patch
from auto_website_visitor.scheduler import SchedulerManager
from auto_website_visitor.logger import VisitorLogger
from auto_website_visitor.config import VisitorSettings


class TestSchedulerManager:
    """Test SchedulerManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        settings = VisitorSettings()
        self.logger = VisitorLogger(settings)
        self.scheduler = SchedulerManager(self.logger)
        self.job_executed = False
        self.execution_count = 0
    
    def teardown_method(self):
        """Clean up after tests."""
        if self.scheduler.is_running():
            self.scheduler.stop()
    
    def test_scheduler_init(self):
        """Test scheduler initialization."""
        assert not self.scheduler.is_running()
        assert self.scheduler.thread is None
    
    def test_parse_interval_seconds(self):
        """Test parsing interval in seconds."""
        assert self.scheduler._parse_interval("30s") == 30
        assert self.scheduler._parse_interval("45") == 45
    
    def test_parse_interval_minutes(self):
        """Test parsing interval in minutes."""
        assert self.scheduler._parse_interval("5m") == 300
        assert self.scheduler._parse_interval("30m") == 1800
    
    def test_parse_interval_hours(self):
        """Test parsing interval in hours."""
        assert self.scheduler._parse_interval("1h") == 3600
        assert self.scheduler._parse_interval("2h") == 7200
    
    def test_parse_interval_days(self):
        """Test parsing interval in days."""
        assert self.scheduler._parse_interval("1d") == 86400
        assert self.scheduler._parse_interval("2d") == 172800
    
    def test_parse_interval_invalid(self):
        """Test parsing invalid interval."""
        with pytest.raises(ValueError):
            self.scheduler._parse_interval("invalid")
    
    def test_schedule_interval_job(self):
        """Test scheduling interval-based job."""
        def test_job():
            self.job_executed = True
        
        # Schedule job with very short interval for testing
        self.scheduler._schedule_interval(test_job, "1s")
        
        assert self.scheduler.is_running()
        
        # Wait for job to execute
        time.sleep(1.5)
        
        assert self.job_executed
        
        self.scheduler.stop()
        assert not self.scheduler.is_running()
    
    def test_schedule_cron_job_invalid(self):
        """Test scheduling with invalid cron expression."""
        def test_job():
            pass
        
        with pytest.raises(ValueError):
            self.scheduler._schedule_cron(test_job, "invalid cron")
    
    def test_scheduler_stop(self):
        """Test stopping scheduler."""
        def test_job():
            time.sleep(0.1)
        
        self.scheduler._schedule_interval(test_job, "1s")
        assert self.scheduler.is_running()
        
        self.scheduler.stop()
        assert not self.scheduler.is_running()
    
    def test_schedule_job_interval(self):
        """Test schedule_job with interval type."""
        def test_job():
            self.execution_count += 1
        
        self.scheduler.schedule_job(test_job, "interval", "1s")
        
        assert self.scheduler.is_running()
        
        # Wait for multiple executions
        time.sleep(2.5)
        
        assert self.execution_count >= 2
        
        self.scheduler.stop()
    
    def test_schedule_job_unsupported_type(self):
        """Test schedule_job with unsupported type."""
        def test_job():
            pass
        
        with pytest.raises(ValueError, match="Unsupported schedule type"):
            self.scheduler.schedule_job(test_job, "unsupported", "1s")
    
    @patch('auto_website_visitor.scheduler.croniter')
    def test_schedule_cron_job_valid(self, mock_croniter):
        """Test scheduling valid cron job."""
        from datetime import datetime, timedelta
        
        # Mock croniter
        mock_cron_instance = Mock()
        mock_cron_instance.get_next.return_value = datetime.now() + timedelta(seconds=1)
        mock_croniter.return_value = mock_cron_instance
        
        def test_job():
            self.job_executed = True
        
        self.scheduler._schedule_cron(test_job, "*/1 * * * *")
        
        assert self.scheduler.is_running()
        
        # Wait for job to potentially execute
        time.sleep(1.5)
        
        self.scheduler.stop()
    
    def test_wait_for_completion_interrupt(self):
        """Test wait_for_completion with keyboard interrupt."""
        def test_job():
            time.sleep(0.1)
        
        self.scheduler._schedule_interval(test_job, "1s")
        
        # Start wait_for_completion in a separate thread
        wait_thread = threading.Thread(target=self.scheduler.wait_for_completion)
        wait_thread.start()
        
        # Simulate KeyboardInterrupt by stopping scheduler
        time.sleep(0.5)
        self.scheduler.stop()
        
        wait_thread.join(timeout=2)
        assert not wait_thread.is_alive()