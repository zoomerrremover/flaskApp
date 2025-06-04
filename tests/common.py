import subprocess
import os
import time


def start_docker_compose(docker_compose_path, detached=True):
    """Starts a Docker Compose server."""
    command = ["docker-compose", "-f", docker_compose_path, "up"]
    if detached:
        command.append("-d")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Docker Compose started successfully.")
        if result.stdout:
            print(result.stdout)
        time.sleep(2)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker Compose (exit code: {e.returncode}):")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"Error: Docker Compose file not found at: {docker_compose_path}")
        return False


def down_docker_compose(docker_compose_path, timeout=None):
    """Stops a Docker Compose server."""
    command = ["docker-compose", "-f", docker_compose_path, "down"]
    if timeout is not None:
        command.extend(["-t", str(timeout)])
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Docker Compose stopped successfully.")
        if result.stdout:
            print(result.stdout)
        time.sleep(2)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Docker Compose (exit code: {e.returncode}):")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"Error: Docker Compose file not found at: {docker_compose_path}")
        return False


if __name__ == "__main__":
    compose_file = os.path.abspath("../docker-compose.yml")  # Adjust path if needed

    print("Starting Docker Compose...")
    if start_docker_compose(compose_file):
        import time

        time.sleep(5)  # Simulate some activity

        print("\nStopping Docker Compose...")
        down_docker_compose(compose_file)
    else:
        print("Failed to start Docker Compose.")
