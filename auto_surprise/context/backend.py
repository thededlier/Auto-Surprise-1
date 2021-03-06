from datetime import datetime
import pathlib

class BackendContextManager():
    def __init__(self, current_path):
        date_time = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        self.temporary_directory = current_path / 'tmp' / date_time

    def __enter__(self):
        self.create_directories()
        return self.temporary_directory

    def __exit__(self, *exc):
        print("Stored temporary files in %s. This can be removed" % (self.temporary_directory.as_posix()))

    def create_directories(self):
        self.temporary_directory.mkdir(parents=True)
