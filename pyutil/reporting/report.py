"""
Main entry point for reporting module.
"""

from pyutil.reporting.logged import logger
from pyutil.errors import PyUtilReportingError
class Reporter:  # TODO: expand from the generated base
    """
    A class used to report messages.

    Attributes
    ----------
    logger : logger
        The logger object used to log messages.
    """
    def __init__(self):
        self.logger = logger

    def report(self, message):
        """
        Log a message.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.info(message)

    def get_reporter(self, reporter: str = 'logger'):
        """
        Get a reporter object.

        Parameters
        ----------
        reporter : str
            The name of the reporter object to get.

        Returns
        -------
        logger
            The logger object.
        """
        if reporter == 'logger':
            return self.logger
        else:
            raise PyUtilReportingError(f"Reporter '{reporter}' not found.")
