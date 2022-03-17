#!/bin/bash
echo "Provided bootstrap execution started..."

sudo yum update -y
echo "yum update completed..."

echo "Git installation started..."
sudo yum install git -y
echo "Git installation completed..."

echo "base packages installed..."

echo "Installing boto3"

pip install boto3

echo "All bootstrap actions completed!"

cd /home/hadoop

pwd

echo "removing the old code if any"
rm -rf my-demo

git clone https://github.com/praveenawstasks/my-demo.git

echo "Cloning my-demo completed!"

cd my-demo