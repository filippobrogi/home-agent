import logging


def configure_logging():
    """
    Configure the logging settings for the application.
    """

    # Add the filename and the line number to the log format to make it easier to debug issues
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
        handlers=[logging.FileHandler("app.log")],
    )
