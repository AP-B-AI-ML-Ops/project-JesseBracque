"""main script to run the entire pipeline"""

# pylint: disable=[W1510]

import subprocess

subprocess.run("python scripts/preprocess_data.py", shell=True)
subprocess.run("python scripts/train.py", shell=True)
subprocess.run("python scripts/hpo.py", shell=True)
subprocess.run("python scripts/register_model.py", shell=True)
