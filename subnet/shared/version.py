import threading
import bittensor as bt

from subnet.version.github_controller import Github
from subnet.version.interpreter_controller import Interpreter


class BaseVersionControl:
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.github = Github()
        self.interpreter = Interpreter()
        self._upgrading = False
        self.must_restart = False

    @property
    def upgrading(self):
        with self._lock:
            return self._upgrading

    @upgrading.setter
    def upgrading(self, value):
        with self._lock:
            self._upgrading = value

    def upgrade_subnet(self, version: str):
        """
        Upgrade the subnet with the requested version or the latest one
        Version has to follow the format major.minor.patch
        """
        try:
            bt.logging.info("[Subnet] Upgrading...")

            # Pull the branch
            self.github.get_tag(f"v{version}")

            # Install dependencies
            self.interpreter.upgrade_dependencies()

            bt.logging.success(f"[Subnet] Upgrade to {version} successful")

            return True
        except Exception as err:
            bt.logging.error(f"[Subnet] Failed to upgrade the subnet: {err}")

        return False

    def downgrade_subnet(self, version: str):
        """
        Downgrade the subnet with the requested version
        Version has to follow the format major.minor.patch
        """
        try:
            # Pull the branch
            self.github.get_tag(f"v{version}")

            # Install dependencies
            self.interpreter.upgrade_dependencies()

            bt.logging.success(f"[Subnet] Downgrade to {version} successful")

            return True
        except Exception as err:
            bt.logging.error(f"[Subnet] Failed to upgrade the subnet: {err}")

        return False
