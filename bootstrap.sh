# Check for Python packages

python3 --version || sudo apt-get install -y python3
pip3 --version || sudo apt-get install -y python3-pip

# Install the AWS IoT Python tooling

pip3 install --user --upgrade AWSIoTPythonSDK
