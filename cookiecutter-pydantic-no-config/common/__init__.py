import logging
import os
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel

log = logging.getLogger("red.your_cog_name.cookiecutter")


class Base(BaseModel):
    @classmethod
    def from_file(cls, path: Path):
        if not path.exists():
            return cls()
        return cls.model_validate_json(path.read_bytes())

    def to_file(self, path: Path) -> None:
        dump = self.model_dump_json(exclude_defaults=True)
        tmp_path = path.parent / f"{path.stem}-{uuid4().fields[0]}.tmp"
        with tmp_path.open(encoding="utf-8", mode="w") as fs:
            fs.write(dump)
            fs.flush()
            os.fsync(fs.fileno())

        try:
            tmp_path.replace(path)
        except FileNotFoundError as e:
            log.error(f"Failed to rename {tmp_path} to {path}", exc_info=e)

        if hasattr(os, "O_DIRECTORY"):
            fd = os.open(path.parent, os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
