import logging
import sys

class ColorFormatter(logging.Formatter):
    COLORS = {
        "SUCCESS": "\033[32m",   # Green
        "INFO": "\033[0m",       # Default
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        reset = self.RESET if color else ""
        formatter = logging.Formatter(
            f"{color}[%(levelname)s] %(message)s{reset}",
            # f"{color}%(asctime)s [%(levelname)s] %(name)s: %(message)s{reset}",
            datefmt="%H:%M:%S"
        )
        return formatter.format(record)


class Logger:
    def __init__(self, name: str = "", verbose: bool = False):
        """
        Centralized logger with color-coded output:
        - success() = green
        - info() = normal
        - warning() = yellow
        - error() = red
        """
        self.logger = logging.getLogger(name)
        log_level = logging.DEBUG if verbose else logging.INFO
        self.logger.setLevel(log_level)

        # Prevent duplicate handlers if multiple Logger instances are created
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(ColorFormatter())
            handler.setLevel(log_level)
            self.logger.addHandler(handler)

        # Adds a custom SUCCESS level between INFO (20) and WARNING (30)
        logging.addLevelName(25, "SUCCESS")

        def success(self, message, *args, **kwargs):
            if self.isEnabledFor(25):
                self._log(25, message, args, **kwargs)
        logging.Logger.success = success

    # Practical methods
    def success(self, msg): self.logger.success(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def debug(self, msg): self.logger.debug(msg)