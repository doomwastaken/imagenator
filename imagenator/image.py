import subprocess


class SyftException(BaseException):
    """Exception while calling syft CLI"""

    pass


class Image:
    def decompose(self, container_name: str) -> str:
        """Generate SBOM of OCI image in JSON format"""
        if not container_name:
            return ""

        print(f"Start generating sbom for image {container_name}")

        out: subprocess.CompletedProcess
        try:
            out = subprocess.run(
                ["syft", f"registry:{container_name}", "-o", "json"],
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as err:
            print(err.stderr)
            raise SyftException

        print("SBOM was generated succefully")

        return out.stdout
