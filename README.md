# 🛠️ Auto Node CLI

A command-line interface for batch installing custom nodes for ComfyUI.

## ✨ Overview

Auto Node CLI is a powerful command-line version of the ComfyUI Custom Node Batch Installer. It simplifies the process of installing multiple custom nodes from GitHub repositories with a single command. Simply provide a text file containing GitHub URLs (one per line), and the tool will handle validation, copying required files, and installation - all from the comfort of your terminal! 🚀

## 🔍 Prerequisites

Before you begin, ensure you have the following installed:

- 🐍 Python 3.6+ installed and in your PATH
- 📦 Git installed and in your PATH
- 💻 ComfyUI already installed on your system

## 🚀 Installation

### Step 1: Get the Code

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/auto_node_cli.git
cd auto_node_cli
```

### Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

Confirm everything is working by checking the version:

```bash
python auto_node_cli.py --version
```

You should see the version information displayed. If you encounter any errors, check the [Troubleshooting](#🔧-troubleshooting) section.

## 📋 Usage Guide

### Basic Usage

The simplest way to use Auto Node CLI is with the following command:

```bash
python auto_node_cli.py -f path/to/urls.txt -d path/to/comfyui/custom_nodes
```

Where:
- `urls.txt` is a text file containing GitHub repository URLs (one per line)
- `path/to/comfyui/custom_nodes` is the path to your ComfyUI's custom_nodes directory

### 🎮 Interactive Mode

If you don't provide the `-d` parameter, the tool will run in interactive mode and prompt you for the custom_nodes directory:

```bash
python auto_node_cli.py -f repositories.txt
# The tool will prompt: "Enter the path to your ComfyUI custom_nodes directory:"
```

## 🔧 Command Line Options

Auto Node CLI provides several command-line options to customize its behavior:

| Option | Description |
|--------|-------------|
| `-f, --file` | Path to text file containing GitHub URLs (one per line). This parameter is **required**. |
| `-d, --dir` | Path to ComfyUI custom_nodes directory. If not provided, you'll be prompted to enter it interactively. |
| `-v, --validate` | Validate inputs without performing installation. Use this to check your configuration before running the actual installation. |
| `--version` | Show the program version and exit. |
| `-h, --help` | Show the help message with all available options and exit. |

### Full Options Example

```bash
# Show help
python auto_node_cli.py -h

# Show version
python auto_node_cli.py --version

# Validate without installing
python auto_node_cli.py -f repos.txt -d C:/ComfyUI/custom_nodes -v

# Full installation with all parameters
python auto_node_cli.py -f repos.txt -d C:/ComfyUI/custom_nodes
```

## 📚 Examples

### 🌟 Basic Installation Example

1. 📝 Create a text file (e.g., `repositories.txt`) with GitHub URLs:

```
https://github.com/username/custom-node-repo1
https://github.com/username/custom-node-repo2
https://github.com/username/custom-node-repo3
```

2. 🚀 Run the installer:

```bash
python auto_node_cli.py -f repositories.txt -d C:/ComfyUI/custom_nodes
```

3. 🎬 The tool will:
   - ✅ Validate the custom_nodes directory
   - ✅ Validate the GitHub URLs
   - 📋 Copy required files to the custom_nodes directory
   - 💾 Save the validated URLs to comfy-repos.txt
   - ❓ Ask for confirmation before starting installation
   - 🔄 Install the custom nodes

4. 👍 Once complete, you'll see a summary of the installation results.

### 🧪 Validation-Only Example

To check your setup without installing (useful for testing):

```bash
python auto_node_cli.py -f repositories.txt -d C:/ComfyUI/custom_nodes -v
```

This will validate the URLs and custom_nodes path without making any changes! 🛡️

### 💡 Windows-Specific Example

On Windows, you might need to use backslashes or quoted paths:

```bash
python auto_node_cli.py -f repositories.txt -d "C:\Users\YourUsername\ComfyUI\custom_nodes"
```

### 🐧 Linux/macOS Example

On Linux or macOS:

```bash
python auto_node_cli.py -f repositories.txt -d ~/comfyui/custom_nodes
```

## 🔄 Complete Installation Process

Here's what happens during the installation process:

1. 📋 **URL Validation**: Each GitHub URL is validated to ensure it's properly formatted
2. 🔍 **Directory Validation**: The custom_nodes directory is checked to ensure it's part of a valid ComfyUI installation
3. 📂 **File Preparation**: Required utility files are copied to the custom_nodes directory
4. 📝 **Repository List**: Valid URLs are saved to a `comfy-repos.txt` file in the custom_nodes directory
5. ✋ **Confirmation**: The tool asks for confirmation before proceeding with installation
6. 📦 **Repository Cloning**: Each GitHub repository is cloned into the custom_nodes directory
7. 🔧 **Package Installation**: Any requirements.txt files in the cloned repositories are processed and dependencies installed
8. 📊 **Summary Report**: A summary of successful and failed installations is displayed

## 🔧 Troubleshooting

### Common Issues

#### ❌ "Error: Path is not a directory"
Ensure the custom_nodes path exists and is a directory. If needed, create it first.

#### ❌ "Error: Directory must be named 'custom_nodes'"
The target directory must be named exactly 'custom_nodes'. Ensure you're pointing to the correct directory.

#### ❌ "Error: Directory does not appear to be a ComfyUI installation"
The parent directory of custom_nodes must contain main.py. Check that you're pointing to a valid ComfyUI installation.

#### ❌ "Error: Git not found"
Ensure Git is installed and in your PATH. Try running `git --version` in your terminal to verify.

#### ❌ "Error cloning [URL]"
Check that the GitHub URL is correct and that you have internet connectivity.

## 📝 Tips for Success

- 🔄 **Keep it Simple**: One URL per line in your input file
- 🧪 **Test First**: Use the `-v` flag to validate before actual installation
- 📋 **Check Logs**: Review the generated log file (named `installer_YYYYMMDD_HHMMSS.log`) for detailed information
- 🔄 **Update URLs**: If a repository has moved, update your URL file accordingly
- 🚫 **Avoid Duplicates**: Remove duplicate URLs from your input file to prevent unnecessary processing

## 📚 Advanced Usage

### Preparing Your Environment

For the best experience:

1. 🔄 Update Git to the latest version
2. 🐍 Use a virtual environment for Python to avoid package conflicts
3. 🔐 Ensure you have sufficient permissions for the target directory

### Integration with Automation

Auto Node CLI can easily be incorporated into scripts or automation workflows:

```bash
# Example bash script
#!/bin/bash
cd /path/to/auto_node_cli
python auto_node_cli.py -f repos.txt -d /path/to/comfyui/custom_nodes < <(echo "y")
```

The `< <(echo "y")` part automatically answers "yes" to the installation confirmation prompt.

## 📊 Requirements

- 🐍 Python 3.6+
- 📦 Git (must be installed and in the PATH)
- 💻 Valid ComfyUI installation with a custom_nodes directory

## 📝 Notes

- ✅ The tool performs thorough validation of paths and URLs before making any changes
- 📋 A detailed log file is created in the current directory for each run
- 🔄 Dependencies from requirements.txt files in cloned repositories are automatically installed
- 📊 The installation process handles errors gracefully, continuing with remaining repositories if one fails
