# Auto Website Visitor

A powerful Python package for automated website visiting with advanced browser automation, scheduling capabilities, and comprehensive configuration options.

> \[!CAUTION]
> This package is designed for legitimate testing and automation purposes. Ensure compliance with website terms of service and applicable laws.

> \[!NOTE]
> This package is under active development. Features and APIs may change in future releases.

![Workflow Status](https://img.shields.io/github/actions/workflow/status/nayandas69/auto-website-visitor/buildpypi.yml?style=flat-square&color=4DB6AC&logo=github)
![Python Version](https://img.shields.io/pypi/pyversions/auto-website-visitor?style=flat-square&color=42A5F5&logo=python)
![PyPI Version](https://img.shields.io/pypi/v/auto-website-visitor?style=flat-square&color=00C853&logo=pypi)
![PyPI Downloads](https://static.pepy.tech/badge/auto-website-visitor) 

## Features

- [x] **Multi-browser Support**: Chrome, Firefox, and Edge
- [x] **Flexible Scheduling**: Interval-based and cron-based scheduling
- [x] **Advanced Browser Options**: Headless mode, custom user agents, proxy support
- [x] **Auto-Scrolling**: Simulate natural browsing behavior
- [x] **Retry Logic**: Configurable retry attempts with delays
- [x] **Comprehensive Logging**: Rotating logs with configurable levels
- [x] **CLI Interface**: Interactive menu and command-line options
- [x] **Configuration Files**: JSON and YAML support
- [x] **Auto-Updates**: Built-in update mechanism
- [x] **Environment Variables**: Support for sensitive configuration

## Installation

```bash
pip install auto-website-visitor
```

## Quick Start

### Basic Usage

```bash
# Visit a website 5 times
awv --url https://example.com --count 5

# Use Firefox in headless mode with auto-scroll
awv --url https://example.com --count 10 --browser firefox --headless --auto-scroll

# Use proxy server
awv --url https://example.com --count 5 --proxy 127.0.0.1:8080
```

### Interactive Mode

```bash
awv --interactive
```

### Using Configuration Files

Create a sample configuration file:

```bash
awv create-config --config-path config.yaml
```

Example configuration (`config.yaml`):

```yaml
url: https://example.com
visit_count: 5
interval: 10
browser: chrome
headless: true
auto_scroll: true
scroll_pause: 1.0
max_scroll: 3
random_delay: true
delay_range: [2, 8]
proxy: 127.0.0.1:8080
retry_attempts: 3
retry_delay: 5
log_level: INFO
log_file: visitor.log
```

Run with configuration:

```bash
awv --config config.yaml
```

### Scheduled Execution

#### Interval-based Scheduling

```bash
# Run every hour
awv --url https://example.com --schedule "1h" --headless

# Run every 30 minutes
awv --url https://example.com --schedule "30m" --headless

# Run every 45 seconds
awv --url https://example.com --schedule "45s" --headless
```

#### Cron-based Scheduling

```bash
# Run every 30 minutes
awv --url https://example.com --schedule "*/30 * * * *" --headless

# Run weekdays at 9 AM
awv --url https://example.com --schedule "0 9 * * 1-5" --headless

# Run every hour during business hours
awv --url https://example.com --schedule "0 9-17 * * 1-5" --headless
```

## Configuration Options

### Core Settings

- `url`: Target website URL (required)
- `visit_count`: Number of visits to perform (default: 1)
- `interval`: Seconds between visits (default: 5)
- `timeout`: Page load timeout in seconds (default: 30)

### Browser Options

- `browser`: Browser to use - chrome, firefox, or edge (default: chrome)
- `headless`: Run browser in headless mode (default: false)
- `user_agent`: Custom user agent string
- `proxy`: Proxy server (format: "ip:port" or "user:pass@ip:port")

### Behavior Settings

- `auto_scroll`: Enable automatic page scrolling (default: false)
- `scroll_pause`: Pause between scroll actions in seconds (default: 0.5)
- `max_scroll`: Maximum number of scroll actions (default: 5)
- `random_delay`: Enable random delays between actions (default: false)
- `delay_range`: Range for random delays in seconds (default: [1, 5])

### Scheduler Settings

- `schedule_enabled`: Enable scheduled execution (default: false)
- `schedule_type`: Schedule type - interval or cron (default: interval)
- `schedule_value`: Schedule value (e.g., "1h", "*/30 * * * *")

### Advanced Options

- `retry_attempts`: Number of retry attempts on failure (default: 3)
- `retry_delay`: Delay between retry attempts in seconds (default: 5)
- `log_level`: Logging level - DEBUG, INFO, WARNING, ERROR (default: INFO)
- `log_file`: Log file path (default: auto_visitor.log)
- `log_rotate`: Enable log rotation (default: true)
- `max_log_size`: Maximum log file size (default: 1MB)
- `backup_count`: Number of backup log files (default: 3)

## Environment Variables

Set sensitive configuration via environment variables:

```bash
export PROXY_USER="username"
export PROXY_PASS="password"
export CUSTOM_HEADERS='{"Authorization": "Bearer token123"}'
```

## CLI Commands

### Main Command

```bash
awv [OPTIONS]
```

### Available Options

- `--url, -u`: Target website URL
- `--count, -c`: Number of visits
- `--interval, -i`: Seconds between visits
- `--browser, -b`: Browser choice (chrome/firefox/edge)
- `--headless`: Run in headless mode
- `--user-agent`: Custom user agent
- `--proxy`: Proxy server
- `--auto-scroll`: Enable auto-scrolling
- `--random-delay`: Enable random delays
- `--config`: Configuration file path
- `--schedule`: Schedule expression
- `--interactive`: Interactive mode
- `--log-level`: Logging level
- `--version`: Show version

### Subcommands

```bash
# Create sample configuration file
awv create-config --config-path config.yaml

# Check for updates
awv update
```

## Python API

Use Auto Website Visitor programmatically:

```python
from auto_website_visitor import AutoWebsiteVisitor, VisitorSettings

# Create settings
settings = VisitorSettings(
    url="https://example.com",
    visit_count=5,
    browser="chrome",
    headless=True,
    auto_scroll=True
)

# Run visitor
visitor = AutoWebsiteVisitor(settings)
success = visitor.run()

# Get statistics
stats = visitor.get_stats()
print(f"Success rate: {stats['success_rate']:.1f}%")
```

### Scheduled Execution

```python
from auto_website_visitor import AutoWebsiteVisitor, VisitorSettings, SchedulerManager
from auto_website_visitor.logger import VisitorLogger

settings = VisitorSettings(url="https://example.com", headless=True)
logger = VisitorLogger(settings)
scheduler = SchedulerManager(logger)

def scheduled_job():
    visitor = AutoWebsiteVisitor(settings)
    visitor.run()

# Schedule every 30 minutes
scheduler.schedule_job(scheduled_job, "interval", "30m")
scheduler.wait_for_completion()
```

## Logging

Auto Website Visitor provides comprehensive logging:

- **Console Output**: Real-time status updates
- **File Logging**: Detailed logs with rotation
- **Configurable Levels**: DEBUG, INFO, WARNING, ERROR
- **Structured Format**: Timestamps and categorized messages

Example log output:

```
2024-01-15 10:30:00 - auto_website_visitor - INFO - Starting Auto Website Visitor
2024-01-15 10:30:00 - auto_website_visitor - INFO - Target URL: https://example.com
2024-01-15 10:30:00 - auto_website_visitor - INFO - Visit count: 5
2024-01-15 10:30:01 - auto_website_visitor - INFO - Starting visit 1/5
2024-01-15 10:30:02 - auto_website_visitor - INFO - Visiting: https://example.com
2024-01-15 10:30:05 - auto_website_visitor - INFO - Website visit completed successfully
```

## Error Handling

The package includes robust error handling:

- **Retry Logic**: Automatic retries on failures
- **Timeout Management**: Configurable page load timeouts
- **Browser Recovery**: Automatic browser restart on crashes
- **Graceful Degradation**: Continues operation despite individual failures

## Security Considerations

- **Proxy Support**: Route traffic through proxy servers
- **User Agent Rotation**: Avoid detection with custom user agents
- **Rate Limiting**: Control visit frequency to avoid overwhelming servers
- **Headless Mode**: Run without visible browser windows

## Performance Tips

1. **Use Headless Mode**: Significantly faster execution
2. **Optimize Intervals**: Balance speed with server courtesy
3. **Configure Timeouts**: Avoid hanging on slow pages
4. **Monitor Resources**: Use appropriate retry settings
5. **Log Management**: Enable rotation for long-running tasks

## Troubleshooting

### Common Issues

1. **WebDriver Not Found**
   ```bash
   # The package automatically downloads drivers, but you can install manually:
   pip install webdriver-manager --upgrade
   ```

2. **Permission Denied**
   ```bash
   # On Linux/Mac, you might need to set executable permissions:
   chmod +x /path/to/chromedriver
   ```

3. **Proxy Authentication**
   ```bash
   # Use environment variables for credentials:
   export PROXY_USER="username"
   export PROXY_PASS="password"
   ```

4. **Memory Issues**
   - Enable headless mode
   - Reduce visit count
   - Increase intervals between visits

### Debug Mode

Enable debug logging for troubleshooting:

```bash
awv --url https://example.com --log-level DEBUG
```

## Updates

Check for and install updates:

```bash
# Check for updates
awv update

# Or use pip directly
pip install --upgrade auto-website-visitor
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

> \[!CAUTION]
> This tool is intended for legitimate testing and automation purposes only. Users are responsible for complying with website terms of service and applicable laws. Always respect robots.txt files and rate limiting guidelines.
