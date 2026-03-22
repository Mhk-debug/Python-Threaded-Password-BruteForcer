🔐 Password Brute-Force Simulator (Python)
📌 Overview

This project is a Python-based password brute-force simulator.

⚙️ Features
Multithreaded password testing using Python's threading module
Queue-based task distribution
Real-time progress animation
Configurable password list (wordlist) input
Simple and extensible code structure

🚀 How It Works
A list of possible passwords (wordlist) is loaded
Tasks are placed into a queue
Multiple threads process the queue simultaneously
Each thread tests passwords until the correct one is found
Progress is displayed in real time
🛠️ Installation & Usage
1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Run the program
python main.py
📂 Wordlist (Important Note)

The password wordlist file is not included in this repository due to its large size and GitHub file limits.

You can use your own wordlist or download a commonly used one such as:

rockyou.txt (widely used for testing and learning purposes)

After downloading, place the file in the project directory and update the file path in the code if necessary.
