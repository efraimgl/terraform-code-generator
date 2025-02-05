import google.generativeai as genai
import os
import logging
import sys
import subprocess  # For formatting Terraform code

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
TERRAFORM_FILE = "generated_infrastructure.tf"
MODEL_NAME = 'gemini-pro'
DEFAULT_AWS_REGION = "us-east-1" # Default region, can be overridden by user input
API_KEY_MIN_LENGTH = 30 # Minimum length of the API key

# Set environment variables (try this, but it might not fix it)
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'
#os.environ['GRPC_POLL_STRATEGY'] = 'epoll1'


def get_api_key():
    """Retrieves and validates the Google API key from the environment."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logging.error("Error: No API_KEY found. Please set the GOOGLE_API_KEY environment variable.")
        sys.exit(1)  # Exit with an error code
    if len(api_key) < API_KEY_MIN_LENGTH:
        logging.error(f"Error: API_KEY is too short (less than {API_KEY_MIN_LENGTH} characters). Please check its value.")
        sys.exit(1)
    return api_key


def generate_terraform_code(prompt, model_name=MODEL_NAME, max_retries=3):
    """Generates Terraform code using the Generative AI model with retry logic."""
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except google.generativeai.APIError as e:
            logging.warning(f"Attempt {attempt+1} failed: Could not connect to the Generative AI API: {e}")
            if attempt == max_retries - 1:  # Last attempt
                logging.error("Max retries reached. Unable to generate code.")
                return None
            # Add exponential backoff (e.g., time.sleep(2**attempt)) if needed for rate limiting
        except Exception as e:
            logging.error(f"Error during code generation: {e}")
            return None
    return None


def save_terraform_code(code, filename=TERRAFORM_FILE, overwrite=False):
    """Saves the Terraform code to a file."""
    if not code:
        logging.warning("No code to save.")
        return

    if os.path.exists(filename) and not overwrite:
        answer = input(f"{filename} already exists. Overwrite? (y/n): ")
        if answer.lower() != 'y':
            print("Code not saved.")
            return

    try:
        with open(filename, "w") as f:
            f.write(code)
        print(f"Terraform code saved to {filename}")
    except OSError as e:
        logging.error(f"Error saving file {filename}: {e}")
        return False  # Indicate failure to save
    return True    # Indicate successful save


def format_terraform_code(filename=TERRAFORM_FILE):
    """Formats the Terraform code using `terraform fmt`."""
    try:
        subprocess.run(["terraform", "fmt", filename], check=True, capture_output=True, text=True)
        print(f"Terraform code formatted in {filename}")
    except FileNotFoundError:
        logging.warning("Terraform CLI not found. Please ensure Terraform is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error formatting Terraform code: {e.stderr}")


def get_aws_region_from_user():
    """Prompts the user for the AWS region."""
    region = input(f"Enter the AWS region (default: {DEFAULT_AWS_REGION}): ").strip()
    if not region:
        region = DEFAULT_AWS_REGION
    return region


def main():
    """Main function to orchestrate the code generation process."""
    api_key = get_api_key()
    genai.configure(api_key=api_key)

    aws_region = get_aws_region_from_user()

    prompt = """You are a helpful AI assistant that generates Terraform code for infrastructure deployment.
    I will describe the infrastructure I need, and you will provide the Terraform code.
    Make sure the code is well-formatted, complete, and ready to be deployed.
    Include comments to explain each section of the code.
    Include a terraform provider block, for example:

    ```terraform
    terraform {
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 4.0"  # Or the latest version you want to use
        }
      }
    }

    provider "aws" {
      region = "us-east-1"
    }
    ```

    # Example Infrastructure:
    Please generate Terraform code for an S3 bucket and a Lambda function.
    """

    # Generate Terraform code using the provided prompt
    terraform_code = generate_terraform_code(prompt)

    if terraform_code:
        save_terraform_code(terraform_code)
        format_terraform_code()
    else:
        logging.error("Failed to generate Terraform code.")

if __name__ == "__main__":
    main()
