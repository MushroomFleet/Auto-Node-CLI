#!/usr/bin/env python3
"""
Auto Node CLI - ComfyUI Custom Node Batch Installer (CLI Version)
This tool helps install multiple custom nodes for ComfyUI from a list of GitHub repositories.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import shutil
import logging
import re
from typing import Tuple, Optional, List
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'installer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

class CustomNodeInstaller:
    """Class for handling the installation of custom ComfyUI nodes."""
    
    def __init__(self):
        # Files required for the installation process
        self.required_files = [
            'clone-custom-nodes.py',
            'package-preparation.py',
            'start-prep.bat'
        ]
        
        # Directory containing utility files
        self.utils_dir = Path(__file__).parent / "utils"

    def validate_path(self, path: str) -> Tuple[bool, str]:
        """
        Validate if the path is a valid ComfyUI custom_nodes directory.
        
        Args:
            path: String path to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if not path or not path.strip():
                return False, "Path cannot be empty!"
            
            path_obj = Path(path)
            
            # Check if path exists
            if not path_obj.exists():
                return False, f"Path does not exist: {path}"
            
            # Check if it's a directory
            if not path_obj.is_dir():
                return False, f"Path is not a directory: {path}"
            
            # Check if it's named 'custom_nodes'
            if path_obj.name != "custom_nodes":
                return False, "Directory must be named 'custom_nodes'"
            
            # Check if it appears to be a ComfyUI custom_nodes directory
            parent_dir = path_obj.parent
            if not (parent_dir / "main.py").exists():
                return False, "Directory does not appear to be a ComfyUI installation (main.py not found in parent directory)"
            
            return True, "Path is valid"
            
        except Exception as e:
            logging.error(f"Path validation error: {str(e)}")
            return False, f"Error validating path: {str(e)}"

    def validate_github_urls(self, urls: List[str]) -> Tuple[bool, str, list]:
        """
        Validate a list of GitHub repository URLs.
        
        Args:
            urls: List of URL strings to validate
            
        Returns:
            Tuple of (is_valid, error_message, valid_urls)
        """
        if not urls:
            return False, "No repository URLs provided", []
        
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            # GitHub URL validation pattern
            pattern = r'^https://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-._]+/?$'
            if re.match(pattern, url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if invalid_urls:
            return False, f"Invalid GitHub URLs found:\n{chr(10).join(invalid_urls)}", valid_urls
        
        return True, "All URLs are valid", valid_urls

    def read_urls_from_file(self, file_path: str) -> Tuple[bool, str, list]:
        """
        Read GitHub repository URLs from a file.
        
        Args:
            file_path: Path to the file containing URLs
            
        Returns:
            Tuple of (success, message, urls)
        """
        try:
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}", []
                
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
                
            if not urls:
                return False, "No URLs found in the file", []
                
            return True, f"Successfully read {len(urls)} URLs from file", urls
                
        except Exception as e:
            logging.error(f"Error reading URLs from file: {str(e)}")
            return False, f"Error reading URLs from file: {str(e)}", []

    def copy_required_files(self, target_path: Path) -> Tuple[bool, str]:
        """
        Copy required installation files to the target directory.
        
        Args:
            target_path: Path object pointing to the target directory
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Use the utils directory as the source
            source_dir = self.utils_dir
            
            if not source_dir.exists():
                return False, f"Utils directory not found: {self.utils_dir}"
            
            for file in self.required_files:
                source = source_dir / file
                if not source.exists():
                    return False, f"Required file not found: {file}"
                shutil.copy2(source, target_path / file)
            
            return True, "Required files copied successfully"
            
        except Exception as e:
            logging.error(f"Error copying files: {str(e)}")
            return False, f"Error copying required files: {str(e)}"

    def save_repos(self, repos: List[str], custom_nodes_path: str) -> Tuple[bool, str]:
        """
        Save repository URLs and prepare installation files.
        
        Args:
            repos: List of repository URLs
            custom_nodes_path: Path to the custom_nodes directory
            
        Returns:
            Tuple of (success, message)
        """
        logging.info(f"Attempting to save repositories to {custom_nodes_path}")
        
        # Validate path
        path_valid, path_msg = self.validate_path(custom_nodes_path)
        if not path_valid:
            return False, f"Error: {path_msg}"
        
        # Validate URLs
        urls_valid, urls_msg, valid_urls = self.validate_github_urls(repos)
        if not urls_valid:
            return False, f"Error: {urls_msg}"
        
        try:
            target_path = Path(custom_nodes_path)
            
            # Copy required files
            copy_success, copy_msg = self.copy_required_files(target_path)
            if not copy_success:
                return False, f"Error: {copy_msg}"
            
            # Save repositories
            with open(target_path / 'comfy-repos.txt', 'w') as f:
                f.write('\n'.join(valid_urls))
            
            logging.info("Repository list saved successfully")
            return True, "Repository list and required files saved successfully!"
            
        except Exception as e:
            logging.error(f"Error saving repositories: {str(e)}")
            return False, f"Error saving repositories: {str(e)}"

    def install_nodes(self, custom_nodes_path: str) -> Tuple[bool, str]:
        """
        Run the node installation process.
        
        Args:
            custom_nodes_path: Path to the custom_nodes directory
            
        Returns:
            Tuple of (success, output)
        """
        logging.info(f"Starting node installation in {custom_nodes_path}")
        
        # Validate path
        path_valid, path_msg = self.validate_path(custom_nodes_path)
        if not path_valid:
            return False, f"Error: {path_msg}"
        
        try:
            script_path = Path(custom_nodes_path) / 'clone-custom-nodes.py'
            if not script_path.exists():
                return False, "Error: clone-custom-nodes.py not found! Please save repository list first."
            
            # Change to the custom_nodes directory to run the script
            current_dir = os.getcwd()
            os.chdir(custom_nodes_path)
            
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True
                )
                
                # Log the complete output
                if result.stdout:
                    logging.info(f"Installation output: {result.stdout}")
                if result.stderr:
                    logging.error(f"Installation errors: {result.stderr}")
                
                formatted_output = ""
                if result.stdout:
                    formatted_output += result.stdout + "\n"
                if result.stderr:
                    formatted_output += "\nErrors:\n" + result.stderr
                
                # Add a clear visual separator and completion message
                formatted_output += "\n" + "="*50 + "\n"
                formatted_output += "Installation process completed!"
                
                logging.info("Installation process completed!")
                
                return result.returncode == 0, formatted_output.strip()
                
            finally:
                # Change back to the original directory
                os.chdir(current_dir)
                
        except Exception as e:
            error_msg = f"Installation error: {str(e)}"
            logging.error(error_msg)
            return False, error_msg


def main():
    """Main entry point for the CLI application."""
    
    # Define command-line arguments
    parser = argparse.ArgumentParser(
        description="Auto Node CLI - ComfyUI Custom Node Batch Installer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Path to text file containing GitHub URLs (one per line)"
    )
    
    parser.add_argument(
        "-d", "--dir",
        required=False,
        help="Path to ComfyUI custom_nodes directory\n" + 
             "(if not specified, will prompt for input)"
    )
    
    parser.add_argument(
        "-v", "--validate",
        action="store_true",
        help="Validate inputs without performing installation"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Auto Node CLI v1.0.0"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    installer = CustomNodeInstaller()
    
    # Read URLs from file
    print(f"Reading URLs from file: {args.file}")
    success, message, urls = installer.read_urls_from_file(args.file)
    
    if not success:
        print(f"Error: {message}")
        sys.exit(1)
    
    print(f"Found {len(urls)} GitHub URLs")
    
    # Validate URLs
    urls_valid, urls_msg, valid_urls = installer.validate_github_urls(urls)
    if not urls_valid:
        print(f"Error: {urls_msg}")
        sys.exit(1)
    
    # Get custom_nodes directory path
    custom_nodes_path = args.dir
    
    if not custom_nodes_path:
        custom_nodes_path = input("Enter the path to your ComfyUI custom_nodes directory: ")
    
    # Validate custom_nodes path
    path_valid, path_msg = installer.validate_path(custom_nodes_path)
    
    if not path_valid:
        print(f"Error: {path_msg}")
        sys.exit(1)
        
    print(f"Path validation: {path_msg}")
    
    # If we're just validating, exit here
    if args.validate:
        print("Validation successful!")
        sys.exit(0)
    
    # Save repositories and prepare installation
    save_success, save_msg = installer.save_repos(valid_urls, custom_nodes_path)
    
    if not save_success:
        print(save_msg)
        sys.exit(1)
    
    print(save_msg)
    
    # Confirm installation
    confirm = input("Ready to install nodes. Continue? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Installation cancelled")
        sys.exit(0)
    
    # Install nodes
    success, output = installer.install_nodes(custom_nodes_path)
    
    print(output)
    
    if not success:
        print("Installation completed with errors. Check the log for details.")
        sys.exit(1)
    
    print("Installation completed successfully!")


if __name__ == "__main__":
    main()
