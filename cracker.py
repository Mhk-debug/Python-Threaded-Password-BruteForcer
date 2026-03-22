import threading
import hashlib
import queue
import os
import time
from termcolor import cprint, colored

NUM_THREADS = os.cpu_count() or 4
PROGRESS_BAR_LENGTH = 30

class PasswordCracker:

    def __init__(self, wordlist_path, hash_function, target_hash):
        self.wordlist_path = wordlist_path
        self.hash_function = hash_function
        self.target_hash = target_hash

        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.found_event = threading.Event()

        self.total_attempts = 0
        self.thread_attempts = {i: 0 for i in range(NUM_THREADS)}

        self.found_password = None
        self.found_by_thread = None

    def load_wordlist(self):
        print("Loading wordlist...")
        start = time.time()

        with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                self.queue.put(line.strip())

        self.total_passwords = self.queue.qsize()

        elapsed = time.time() - start
        print(f"Loaded {self.total_passwords:,} passwords in {elapsed:.2f}s\n")

    def show_progress(self, start_time):
        elapsed = time.time() - start_time

        percent = self.total_attempts / self.total_passwords
        filled = int(PROGRESS_BAR_LENGTH * percent)

        bar = "█" * filled + "░" * (PROGRESS_BAR_LENGTH - filled)

        speed = self.total_attempts / elapsed if elapsed > 0 else 0
        remaining = self.total_passwords - self.total_attempts
        eta = remaining / speed if speed > 0 else 0

        print(
            f"\r|{bar}| {percent*100:6.2f}% | {speed:8.0f}/s | ETA {eta:6.1f}s",
            end="",
            flush=True,
        )

    def worker(self, thread_id, start_time):

        while not self.found_event.is_set():

            try:
                guess = self.queue.get_nowait()
            except queue.Empty:
                return

            guess_hash = self.hash_function(guess.encode()).hexdigest()

            with self.lock:
                self.thread_attempts[thread_id] += 1
                self.total_attempts += 1

                if self.total_attempts % 50 == 0:
                    self.show_progress(start_time)

            if guess_hash == self.target_hash:
                with self.lock:
                    if not self.found_event.is_set():
                        self.found_password = guess
                        self.found_by_thread = thread_id
                        self.found_event.set()
                return

            self.queue.task_done()

    def start(self):

        start_time = time.time()

        threads = [
            threading.Thread(target=self.worker, args=(i, start_time))
            for i in range(NUM_THREADS)
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        return time.time() - start_time

    def show_results(self, elapsed):

        if self.found_event.is_set():
            print(colored(f"\n\nPassword found: {self.found_password}", "blue"))
            cprint(f"Found by thread: {self.found_by_thread}", "green", attrs=["bold"])
        else:
            print(colored("\n\nPassword not found in wordlist.", "red"))

        cprint("\nStatistics", "yellow", attrs=["bold", "underline"])

        print(f"Total guesses: {self.total_attempts:,}")
        print(f"Time taken: {elapsed:.2f} seconds")

        if elapsed > 0:
            print(f"Average speed: {int(self.total_attempts/elapsed):,} guesses/sec")

        cprint("Thread statistics:", attrs=["bold", "underline"])

        for thread_id, attempts in self.thread_attempts.items():
            print(f"Thread {thread_id}: {attempts:,} guesses")


def choose_password():

    while True:
        password = input("Enter password: ").strip()
        if password:
            return password


def choose_hash_algorithm():

    algorithms = {
        "1": hashlib.md5,
        "2": hashlib.sha1,
        "3": hashlib.sha256,
    }

    print("Choose hash algorithm")
    print("1 - MD5")
    print("2 - SHA1")
    print("3 - SHA256")

    return algorithms.get(input("Choice: ").strip())


def main():

    password = choose_password()
    hash_function = choose_hash_algorithm()

    if not hash_function:
        print("Invalid algorithm.")
        return

    target_hash = hash_function(password.encode()).hexdigest()

    cracker = PasswordCracker("sample_wordlist.txt", hash_function, target_hash)

    cprint("Password Cracker", "cyan", attrs=["bold", "underline"])
    print("Target hash:", target_hash)
    print("Algorithm:", hash_function.__name__)
    print("Threads:", NUM_THREADS, "\n")

    cracker.load_wordlist()

    if input("Type 'start' to begin: ").strip().lower() != "start":
        return

    print("\nStarting...\n")

    elapsed = cracker.start()
    cracker.show_results(elapsed)


if __name__ == "__main__":
    main()