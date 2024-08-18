import time
import signal
import sys
from micro_update_manager.config_loader import load_config
from micro_update_manager.package_updater import monitor_packages
from micro_update_manager.process_manager import restart_processes


def main():
    """
    Main function to load configuration and start the update manager.
    """
    # Load the configuration from the config.yaml file
    config = load_config('config.yaml')

    # Retrieve the loop refresh interval from the configuration
    refresh_interval = config.get("refresh_interval", 3600)  # Default to 3600 seconds (1 hour) if not specified

    def signal_handler(sig, frame):
        print('Shutting down gracefully...')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Main loop to monitor and update packages according to the configuration
    while True:
        try:
            updated_packages = monitor_packages(config)
            for package in updated_packages:
                if package["requires_restart"]:
                    restart_processes(package["processes_to_restart"], config)
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(refresh_interval)  # Use the configured refresh interval


if __name__ == "__main__":
    main()
