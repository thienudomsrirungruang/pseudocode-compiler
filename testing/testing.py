import os
import shutil
import sys
import time
import subprocess

FOLDER_PATH = os.path.abspath(os.path.join(__file__, '../..'))
EXEC_PATH = os.path.abspath(os.path.join(FOLDER_PATH, 'main.py'))
INPUT_PATH = os.path.abspath(os.path.join(FOLDER_PATH, 'input.pdc'))
OUTPUT_PATH = os.path.abspath(os.path.join(FOLDER_PATH, 'output.py'))
TEST_INPUT_PATH = os.path.abspath(os.path.join(FOLDER_PATH, 'testing/test-code.pdc'))
EXPECTED_OUTPUT_PATH = os.path.abspath(os.path.join(FOLDER_PATH, 'testing/test-output.txt'))

if __name__ == '__main__':
    print('This script executes arbritary python code generated from a potentially buggy program and may cause issues.')
    print('I am not responsible for any damage caused.')
    input('Enter to continue')
    
    # copies test pseudocode file to actual input file
    print("Copying input...")
    with open(TEST_INPUT_PATH, 'rb') as f:
        pdc = f.read()
    with open(INPUT_PATH, 'wb') as f:
        f.write(pdc)
        f.flush()
    time.sleep(3)

    # run the program
    print("Running the program...")
    proc = subprocess.Popen([sys.executable, EXEC_PATH], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    time.sleep(3)

    # run the compiled program
    print("Running the compiled program...")
    proc = subprocess.Popen([sys.executable, OUTPUT_PATH], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    program_output = proc.communicate()[0]
    split_lines = program_output.splitlines()
    
    # check the output against the file
    print("Checking output against the file...")
    i = 1
    errors = 0
    with open(EXPECTED_OUTPUT_PATH, 'r') as f:
        for line in split_lines:
            line = line.decode('utf-8')
            expected_line = f.readline()[:-1]
            if line != expected_line:
                print(f'line {i}: Expected "{expected_line}", got "{line}"')
                errors += 1
            i += 1
    if errors == 0:
        print("All ok!")
    else:
        print(f"{errors} errors found.")

