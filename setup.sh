#!/bin/bash
# setup.sh: Set up the environment for running your Python code on Termux.
# This script updates the system, installs required packages and dependencies,
# including Python, wget, unzip, openjdk-17, apksigner, python-pillow, and Apktool.
# It is intended to run on Termux only.

# Color definitions for log messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# Ensure the script is running on Termux by checking for the "pkg" command
if ! command -v pkg >/dev/null 2>&1; then
    echo -e "${RED}[ERROR] This script is intended to run on Termux only. Exiting.${NC}"
    exit 1
fi

echo -e "${BLUE}===== Starting Termux Setup =====${NC}"

# Update package lists and upgrade all installed packages
echo -e "${YELLOW}[INFO] Updating package lists...${NC}"
pkg update && pkg upgrade -y

# Install required packages
echo -e "${YELLOW}[INFO] Installing required packages: python, wget, unzip, openjdk-17, apksigner, python-pillow...${NC}"
pkg install python3 wget unzip openjdk-17 apksigner python-pillow -y

# Upgrade pip and install Python dependencies
echo -e "${BLUE}[INFO] Upgrading pip and installing Python dependencies...${NC}"
if ! command -v pip >/dev/null 2>&1; then
    echo -e "${YELLOW}[WARN] pip not found. Checking for pip3...${NC}"
    if command -v pip3 >/dev/null 2>&1; then
        alias pip=pip3
        echo -e "${GREEN}[INFO] pip3 found. Using pip3.${NC}"
    else
        echo -e "${RED}[ERROR] pip is not installed. Exiting.${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}[INFO] Installing Python package: colorama...${NC}"
pip install colorama

# Install Apktool using the provided command
echo -e "${BLUE}[INFO] Installing Apktool...${NC}"
curl -s https://raw.githubusercontent.com/rendiix/termux-apktool/main/install.sh | bash

echo -e "${GREEN}[INFO] Apktool installed successfully.${NC}"

echo -e "${GREEN}===== Termux Setup Completed Successfully! =====${NC}"
