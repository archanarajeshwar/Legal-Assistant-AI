import logging
import sys


logging.basicConfig(
		format='%(asctime)s %(levelname)s %(message)s',
		datefmt='%Y/%m/%d %H:%M:%S',
		level=logging.INFO
	)


def progress_bar(current: int, total: int, prefix: str = "", suffix: str = "", bar_length: int = 40):
    if total <= 0:
        return
    
    frac = max(0.0, min(1.0, current / total))
    filled = int(bar_length * frac)
    bar = "█" * filled + "-" * (bar_length - filled)
    percent = round(frac * 100, 1)
    progress_line = f"\r{prefix}|{bar}| {percent}% ({current}/{total}) {suffix}"
    
    sys.stdout.write(progress_line.ljust(80))
    sys.stdout.flush()
    
    if current >= total:
        sys.stdout.write("\n")
        sys.stdout.flush()