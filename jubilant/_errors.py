import subprocess


class RunError(subprocess.CalledProcessError):
    """Subclass of CalledProcessError that includes stdout/stderr in the string."""

    def __str__(self):
        s = super().__str__()
        if self.stdout:
            s += '\nStdout:\n' + self.stdout
        if self.stderr:
            s += '\nStderr:\n' + self.stderr
        return s
