import traceback
import datetime



class TestException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class WikiSearchPageError(Exception):
    def __init__(self, search_query:str, cause=None):
        if search_query:
            self.err_header = "Error while searching for page with query: " + search_query + " ->"
            self.cause = cause if cause else self.err_header
            self.message = self.err_header + " " + self.cause
        else:
            raise ValueError("Some error occurred while searching for page")
        super().__init__(f"{self.__class__.__name__}: {self.message}")

class PageError(Exception):
    def __init__(self, page, message):
        if not page:
            raise ValueError("Page cannot be None")
        else:
            self.page = page
            self.err_header = "Error while processing page: " + str(page)
            self.message = self.err_header + " " + message
            super().__init__(self.message)



def with_time_log(func):
    """Decorator factory to log the time of the function call"""
    def decorator(logs_path: str, *args, **kwargs):
        with open(logs_path, mode='a') as f:
            f.write(f"Time: {datetime.datetime.now()}\n")
        return func(logs_path, *args, **kwargs)
    return decorator


@with_time_log
def handle_error(logs_path: str, e: Exception):
    """Log the error to logfile"""
    traceback_str = ''.join(traceback.format_tb(e.__traceback__))
    with open(logs_path, 'a') as f:
        # Write date and time of the error
        f.write(f'Error: {e}\n')
        f.write(f'Traceback: {traceback_str}\n')



        

    