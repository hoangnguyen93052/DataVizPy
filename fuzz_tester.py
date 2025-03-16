import random
import string
import json
import tempfile
import subprocess
import os
import time
from typing import Any, Callable, List, Dict


class FuzzTester:
    def __init__(self, target_function: Callable[[Any], Any], max_length: int = 100):
        self.target_function = target_function
        self.max_length = max_length
        self.test_cases = []
    
    def generate_random_string(self) -> str:
        length = random.randint(1, self.max_length)
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

    def generate_test_cases(self, num_cases: int) -> None:
        for _ in range(num_cases):
            self.test_cases.append(self.generate_random_string())
    
    def run_tests(self) -> List[Dict[str, Any]]:
        results = []
        for case in self.test_cases:
            try:
                result = self.target_function(case)
                results.append({'input': case, 'output': result, 'error': None})
            except Exception as e:
                results.append({'input': case, 'output': None, 'error': str(e)})
        return results

    def save_results(self, results: List[Dict[str, Any]], filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)


def example_function(input_data: Any) -> str:
    if isinstance(input_data, str) and len(input_data) > 0:
        return f"Processed: {input_data}"
    raise ValueError("Invalid input")


def main():
    tester = FuzzTester(example_function)
    tester.generate_test_cases(100)
    results = tester.run_tests()
    tester.save_results(results, 'fuzz_test_results.json')


if __name__ == "__main__":
    main()


class CommandFuzzer:
    def __init__(self, command: str, input_generator: Callable[[], str], max_attempts: int = 100):
        self.command = command
        self.input_generator = input_generator
        self.max_attempts = max_attempts

    def run_command(self, input_data: str) -> subprocess.CompletedProcess:
        process = subprocess.run(self.command, input=input_data.encode(), capture_output=True, text=True, shell=True)
        return process

    def fuzz(self) -> List[Dict[str, Any]]:
        results = []
        for _ in range(self.max_attempts):
            input_data = self.input_generator()
            result = self.run_command(input_data)
            results.append({
                'input': input_data,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
            })
        return results


def command_input_generator() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(1, 50)))


def main_command_fuzzer():
    command = "echo"  # Example command
    fuzzer = CommandFuzzer(command(command_input_generator, 5)
    results = fuzzer.fuzz()
    fuzzer.save_results(results, 'command_fuzz_results.json')


if __name__ == "__main__":
    main_command_fuzzer()


def save_command_results(results: List[Dict[str, Any]], filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)


def advanced_example_function(input_data: Any) -> str:
    if isinstance(input_data, str) and len(input_data) > 0:
        if "fail" in input_data:
            raise ValueError("Intentional failure for fuzz testing")
        return f"Processed Info: {input_data}"
    raise ValueError("Invalid input type")


def main_advanced_fuzzer():
    tester = FuzzTester(advanced_example_function)
    tester.generate_test_cases(100)
    results = tester.run_tests()
    tester.save_results(results, 'advanced_fuzz_test_results.json')


if __name__ == "__main__":
    main_advanced_fuzzer()


class FuzzerConfig:
    def __init__(self, target_function: Callable[[Any], Any], num_cases: int, output_file: str):
        self.target_function = target_function
        self.num_cases = num_cases
        self.output_file = output_file

    def create_tester(self) -> FuzzTester:
        return FuzzTester(self.target_function)

    def execute(self) -> None:
        tester = self.create_tester()
        tester.generate_test_cases(self.num_cases)
        results = tester.run_tests()
        tester.save_results(results, self.output_file)


if __name__ == "__main__":
    config = FuzzerConfig(advanced_example_function, 100, 'fuzzer_config_results.json')
    config.execute()


class FileFuzzer:
    def __init__(self, target_function: Callable[[List[str]], Any], file_path: str):
        self.target_function = target_function
        self.file_path = file_path

    def read_file(self) -> List[str]:
        with open(self.file_path, 'r') as file:
            return file.readlines()

    def fuzz_file(self) -> List[Dict[str, Any]]:
        results = []
        lines = self.read_file()
        for line in lines:
            line = line.strip()
            if line:
                try:
                    result = self.target_function(line)
                    results.append({'input': line, 'output': result, 'error': None})
                except Exception as e:
                    results.append({'input': line, 'output': None, 'error': str(e)})
        return results


def main_file_fuzzer():
    file_fuzzer = FileFuzzer(advanced_example_function, 'input_file.txt')
    results = file_fuzzer.fuzz_file()
    file_fuzzer.save_results(results, 'file_fuzz_results.json')


if __name__ == "__main__":
    main_file_fuzzer()


class RandomJsonFuzzer:
    def __init__(self, target_function: Callable[[Any], Any], json_structure: Dict[str, List[Any]], num_cases: int):
        self.target_function = target_function
        self.json_structure = json_structure
        self.num_cases = num_cases

    def generate_random_json(self) -> Dict[str, Any]:
        random_json = {}
        for key, value in self.json_structure.items():
            random_json[key] = random.choice(value)
        return random_json

    def fuzz(self) -> List[Dict[str, Any]]:
        results = []
        for _ in range(self.num_cases):
            random_json = self.generate_random_json()
            try:
                result = self.target_function(random_json)
                results.append({'input': random_json, 'output': result, 'error': None})
            except Exception as e:
                results.append({'input': random_json, 'output': None, 'error': str(e)})
        return results


def json_function(input_data: Dict[str, Any]) -> str:
    if 'name' in input_data and isinstance(input_data['name'], str):
        return f"Hello, {input_data['name']}!"
    raise ValueError("Invalid JSON structure")


def main_json_fuzzer():
    json_structure = {
        'name': ['Alice', 'Bob', None, '', 123, 'Charlie'],
        'age': [22, None, 'twenty', 5],
        'city': ['New York', 'London', None, '', 'Tokyo'],
    }
    fuzzer = RandomJsonFuzzer(json_function, json_structure, 100)
    results = fuzzer.fuzz()
    fuzzer.save_results(results, 'json_fuzz_results.json')


if __name__ == "__main__":
    main_json_fuzzer()


class TimeoutFuzzTester(FuzzTester):
    def __init__(self, target_function: Callable[[Any], Any], max_length: int, timeout: int):
        super().__init__(target_function, max_length)
        self.timeout = timeout

    def run_tests(self) -> List[Dict[str, Any]]:
        results = []
        for case in self.test_cases:
            try:
                result = self.run_with_timeout(case)
                results.append({'input': case, 'output': result, 'error': None})
            except Exception as e:
                results.append({'input': case, 'output': None, 'error': str(e)})
        return results

    def run_with_timeout(self, case: Any) -> Any:
        import signal

        def handler(signum, frame):
            raise TimeoutError("Function call timed out")

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.timeout)
        try:
            result = self.target_function(case)
        finally:
            signal.alarm(0)  # Disable the alarm
        return result


def slow_function(input_data: str) -> str:
    time.sleep(random.uniform(0.1, 1.0))  # Simulates a delay
    return f"Slow Processed Info: {input_data}"


def main_timeout_fuzzer():
    timeout_tester = TimeoutFuzzTester(slow_function, 100, timeout=0.5)
    timeout_tester.generate_test_cases(50)
    results = timeout_tester.run_tests()
    timeout_tester.save_results(results, 'timeout_fuzz_results.json')


if __name__ == "__main__":
    main_timeout_fuzzer()