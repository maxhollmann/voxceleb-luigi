from pathlib import Path
import random


class AtomizedLocalTarget:
    def __init__(self, local_target):
        self.local_target = local_target

        target_path = Path(local_target.path)
        rand = random.randint(0, 2**32)
        self.path = target_path.parent / f"{target_path.stem}.tmp{rand}{target_path.suffix}"

        self.failed = False

    def fail(self):
        self.failed = True


    def __del__(self):
        self._remove_tempfile()


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is None and not self.failed:
            self._finalize()
        else:
            self._remove_tempfile()


    def _remove_tempfile(self):
        if self.path.exists():
            self.path.unlink()

    def _finalize(self):
        self.local_target.fs.rename_dont_move(str(self.path), self.local_target.path)
