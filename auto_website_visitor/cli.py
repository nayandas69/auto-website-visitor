#!/usr/bin/env python3

"""Command Line Interface for Auto Website Visitor."""

import os
import sys
import click
from typing import Optional

from . import __version__
from .config import Config, VisitorSettings
from .core import AutoWebsiteVisitor
from .scheduler import SchedulerManager
from .logger import VisitorLogger
from .updater import AutoUpdater


@click.group(invoke_without_command=True)
@click.option("--url", "-u", help="Target website URL")
@click.option("--count", "-c", type=int, help="Number of visits")
@click.option("--interval", "-i", type=int, help="Seconds between visits")
@click.option(
    "--browser",
    "-b",
    type=click.Choice(["chrome", "firefox", "edge"]),
    help="Browser to use",
)
@click.option("--headless", is_flag=True, help="Run browser in headless mode")
@click.option("--user-agent", help="Custom user agent string")
@click.option("--proxy", help="Proxy server (ip:port or user:pass@ip:port)")
@click.option("--auto-scroll", is_flag=True, help="Enable automatic scrolling")
@click.option(
    "--random-delay", is_flag=True, help="Enable random delays between actions"
)
@click.option("--config", help="Configuration file path")
@click.option("--schedule", help="Schedule expression (cron or interval)")
@click.option("--interactive", is_flag=True, help="Run in interactive mode")
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    help="Logging level",
)
@click.option("--version", is_flag=True, help="Show version information")
@click.pass_context
def main(ctx, **kwargs):
    """Auto Website Visitor - Automated website visiting with advanced features."""

    # FIX: Check if this is a subcommand call - if so, don't process main logic
    if ctx.invoked_subcommand is not None:
        return
    if kwargs.get("version"):
        click.echo(f"Auto Website Visitor v{__version__}")
        return

    if kwargs.get("interactive"):
        interactive_mode()
        return

    # Load configuration
    config = Config(kwargs.get("config"))

    # Update settings from command line arguments - Fix: properly map 'count' to 'visit_count'
    args_mapping = {}
    for k, v in kwargs.items():
        if v is not None:
            # Map CLI argument names to settings attribute names
            if k == "count":
                args_mapping["visit_count"] = v  # Fix: map --count to visit_count
            elif k == "auto_scroll":
                args_mapping["auto_scroll"] = v  # Fix: map --auto-scroll to auto_scroll
            elif k == "random_delay":
                args_mapping["random_delay"] = (
                    v  # Fix: map --random-delay to random_delay
                )
            elif k == "user_agent":
                args_mapping["user_agent"] = v  # Fix: map --user-agent to user_agent
            elif k == "log_level":
                args_mapping["log_level"] = v  # Fix: map --log-level to log_level
            else:
                args_mapping[k] = v

    config.update_from_args(**args_mapping)

    try:
        config.validate()
    except ValueError as e:
        click.echo(f"Configuration error: {e}", err=True)
        sys.exit(1)

    # Check for schedule mode
    if kwargs.get("schedule"):
        run_scheduled(config, kwargs["schedule"])
    else:
        # Run normal mode
        if not config.settings.url:
            click.echo("Error: URL is required. Use --url or --interactive", err=True)
            sys.exit(1)

        run_visitor(config)


def run_visitor(config: Config) -> None:
    """Run the website visitor.

    Args:
        config: Configuration instance
    """
    visitor = AutoWebsiteVisitor(config.settings)
    success = visitor.run()

    if not success:
        sys.exit(1)


def run_scheduled(config: Config, schedule_expr: str) -> None:
    """Run visitor in scheduled mode.

    Args:
        config: Configuration instance
        schedule_expr: Schedule expression
    """
    logger = VisitorLogger(config.settings)
    scheduler = SchedulerManager(logger)

    def scheduled_job():
        visitor = AutoWebsiteVisitor(config.settings)
        visitor.run()

    try:
        # Determine schedule type
        if any(char in schedule_expr for char in ["*", "/", "-", ","]):
            schedule_type = "cron"
        else:
            schedule_type = "interval"

        scheduler.schedule_job(scheduled_job, schedule_type, schedule_expr)

        click.echo(f"Scheduled visitor started with {schedule_type}: {schedule_expr}")
        click.echo("Press Ctrl+C to stop...")

        scheduler.wait_for_completion()

    except KeyboardInterrupt:
        click.echo("\nStopping scheduled visitor...")
        scheduler.stop()
    except Exception as e:
        click.echo(f"Scheduler error: {e}", err=True)
        sys.exit(1)


def interactive_mode() -> None:
    """Run in interactive mode."""
    click.echo("=== Auto Website Visitor - Interactive Mode ===\n")

    config = Config()

    while True:
        click.echo("1. Configure and run visitor")
        click.echo("2. Load configuration file")
        click.echo("3. Save current configuration")
        click.echo("4. Check for updates")
        click.echo("5. Exit")

        choice = click.prompt("\nSelect an option", type=int)

        if choice == 1:
            configure_and_run(config)
        elif choice == 2:
            load_config_interactive(config)
        elif choice == 3:
            save_config_interactive(config)
        elif choice == 4:
            check_updates_interactive(config)
        elif choice == 5:
            click.echo("Goodbye!")
            break
        else:
            click.echo("Invalid option. Please try again.\n")


def configure_and_run(config: Config) -> None:
    """Configure settings and run visitor interactively."""
    click.echo("\n=== Configuration ===")

    # Basic settings
    url = click.prompt(
        "Website URL", default=config.settings.url or "https://example.com"
    )
    config.settings.url = url

    count = click.prompt(
        "Number of visits", type=int, default=config.settings.visit_count
    )
    config.settings.visit_count = count

    interval = click.prompt(
        "Interval between visits (seconds)", type=int, default=config.settings.interval
    )
    config.settings.interval = interval

    # Browser settings
    browser = click.prompt(
        "Browser",
        type=click.Choice(["chrome", "firefox", "edge"]),
        default=config.settings.browser,
    )
    config.settings.browser = browser

    headless = click.confirm("Run in headless mode?", default=config.settings.headless)
    config.settings.headless = headless

    # Advanced options
    if click.confirm("Configure advanced options?", default=False):
        configure_advanced_options(config)

    # Schedule options
    if click.confirm("Enable scheduling?", default=False):
        configure_scheduling(config)

    try:
        config.validate()

        if config.settings.schedule_enabled:
            run_scheduled(config, config.settings.schedule_value)
        else:
            run_visitor(config)

    except ValueError as e:
        click.echo(f"Configuration error: {e}", err=True)
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user")


def configure_advanced_options(config: Config) -> None:
    """Configure advanced options interactively."""
    click.echo("\n=== Advanced Options ===")

    auto_scroll = click.confirm(
        "Enable auto-scroll?", default=config.settings.auto_scroll
    )
    config.settings.auto_scroll = auto_scroll

    random_delay = click.confirm(
        "Enable random delays?", default=config.settings.random_delay
    )
    config.settings.random_delay = random_delay

    user_agent = click.prompt(
        "Custom user agent (leave empty for default)",
        default=config.settings.user_agent or "",
        show_default=False,
    )
    config.settings.user_agent = user_agent if user_agent else None

    proxy = click.prompt(
        "Proxy server (leave empty for none)",
        default=config.settings.proxy or "",
        show_default=False,
    )
    config.settings.proxy = proxy if proxy else None

    retry_attempts = click.prompt(
        "Retry attempts", type=int, default=config.settings.retry_attempts
    )
    config.settings.retry_attempts = retry_attempts

    log_level = click.prompt(
        "Log level",
        type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
        default=config.settings.log_level,
    )
    config.settings.log_level = log_level


def configure_scheduling(config: Config) -> None:
    """Configure scheduling options interactively."""
    click.echo("\n=== Scheduling Options ===")

    config.settings.schedule_enabled = True

    schedule_type = click.prompt(
        "Schedule type",
        type=click.Choice(["interval", "cron"]),
        default=config.settings.schedule_type,
    )
    config.settings.schedule_type = schedule_type

    if schedule_type == "interval":
        click.echo("Examples: 1h, 30m, 45s")
        schedule_value = click.prompt(
            "Interval", default=config.settings.schedule_value
        )
    else:
        click.echo(
            "Examples: */30 * * * * (every 30 minutes), 0 9 * * 1-5 (weekdays at 9 AM)"
        )
        schedule_value = click.prompt("Cron expression", default="*/30 * * * *")

    config.settings.schedule_value = schedule_value


def load_config_interactive(config: Config) -> None:
    """Load configuration file interactively."""
    config_path = click.prompt(
        "Configuration file path", default=config.get_default_config_path()
    )

    try:
        config.load_config(config_path)
        click.echo(f"Configuration loaded from: {config_path}")
    except FileNotFoundError:
        click.echo(f"Configuration file not found: {config_path}", err=True)
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)


def save_config_interactive(config: Config) -> None:
    """Save configuration file interactively."""
    config_path = click.prompt(
        "Save configuration to", default=config.get_default_config_path()
    )
    format_type = click.prompt(
        "Format", type=click.Choice(["yaml", "json"]), default="yaml"
    )

    try:
        config.save_config(config_path, format_type)
        click.echo(f"Configuration saved to: {config_path}")
    except Exception as e:
        click.echo(f"Error saving configuration: {e}", err=True)


def check_updates_interactive(config: Config) -> None:
    """Check for updates interactively."""
    logger = VisitorLogger(config.settings)
    updater = AutoUpdater(logger, __version__)

    current_version, latest_version = updater.get_version_info()

    click.echo(f"Current version: {current_version}")

    if latest_version:
        click.echo(f"Latest version: {latest_version}")
        if click.confirm("Update now?"):
            if updater.update_package(latest_version):
                click.echo("Update completed successfully!")
                click.echo("Please restart the application to use the new version.")
            else:
                click.echo("Update failed. Please check the logs for details.")
    else:
        click.echo("You are using the latest version.")


@click.command()
@click.option("--config-path", help="Path to create sample configuration")
def create_config(config_path: Optional[str] = None):
    """Create a sample configuration file."""
    # FIX: Create a new Config instance without requiring URL validation
    # This allows create-config to work without needing a URL
    config = Config()

    if not config_path:
        config_path = config.get_default_config_path()

    try:
        config.create_sample_config(config_path)
        click.echo(f"Sample configuration created: {config_path}")
    except Exception as e:
        click.echo(f"Error creating configuration: {e}", err=True)


@click.command()
def update():
    """Check for and install updates."""
    # FIX: Create a minimal settings instance for the updater
    # This allows update command to work without requiring URL validation
    settings = VisitorSettings()
    logger = VisitorLogger(settings)
    updater = AutoUpdater(logger, __version__)

    latest_version = updater.check_for_updates()

    if latest_version:
        click.echo(f"Update available: {__version__} -> {latest_version}")
        if click.confirm("Install update?"):
            if updater.update_package(latest_version):
                click.echo("Update completed successfully!")
            else:
                click.echo("Update failed. Please check the logs.")
    else:
        click.echo("No updates available.")


# Add subcommands
main.add_command(create_config)
main.add_command(update)


if __name__ == "__main__":
    main()
