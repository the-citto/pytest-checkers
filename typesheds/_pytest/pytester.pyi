import builtins
import pathlib
import typing

class RunResult(typing.Protocol):
    ret: int
    stdout: LineMatcher
    stderr: LineMatcher
    def assert_outcomes(
        self,
        passed: int = 0,
        skipped: int = 0,
        failed: int = 0,
        errors: int = 0,
        xpassed: int = 0,
        xfailed: int = 0,
    ) -> None: ...

class LineMatcher(typing.Protocol):
    def fnmatch_lines(self, lines2check: list[builtins.str], *, consecutive: bool = False) -> None: ...
    def no_fnmatch_line(self, pat: builtins.str) -> None: ...
    def str(self) -> builtins.str: ...

class Pytester:
    def makepyfile(self, *args: str, **kwargs: str) -> pathlib.Path: ...
    def runpytest_subprocess(self, *args: str) -> RunResult: ...
