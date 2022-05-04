import typing
import subprocess


class Cache:
    """Basic cache class"""


class InMemoryCache(Cache):
    """InMemory cache"""
    MAX_LENGTH = 1000

    def __init__(self) -> None:
        self.cache: dict = {}
        
    def cache_or_call(self, container_name, func):
        out: subprocess.CompletedProcess
        try:
            out = subprocess.run(
                ["md5sum", container_name],
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as err:
            print(err.stderr)
            raise

        md5sum = out.stdout.split()[0].strip()
        if md5sum not in self.cache:
            if len(self.cache) >= self.MAX_LENGTH:
                # pop random element
                random_item = list(self.cache)[0]
                del self.cache[random_item]
            
            self.cache[md5sum] = func(container_name)
        
        return self.cache[md5sum]
