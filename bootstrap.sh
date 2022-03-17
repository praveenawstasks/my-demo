#!/bin/bash
echo "Provided bootstrap execution started..."

sudo yum update -y
echo "yum update completed..."

echo "Git installation started..."
sudo yum install git -y
echo "Git installation completed..."

echo "base packages installed..."

cd /home/hadoop

pwd

echo "removing the old code if any"
rm -rf my-demo

git clone https://github.com/praveenawstasks/my-demo.git

echo "Cloning my-demo completed!"

cd my-demo

echo "Installing boto3"
sudo python3 -m pip install boto3
echo "Installing boto3 completed"

echo "All bootstrap actions completed!..."