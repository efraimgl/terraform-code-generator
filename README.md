# terraform-code-generator
Automating Terraform Code Generation with Google Generative AI and Python

Certainly! Here's a README file you can use for your project:

---

# Terraform Code Generator

This Python script generates Terraform code using the Google Generative AI model, formats it, and saves it to a file. The Terraform code is generated based on a user-provided prompt, which describes the infrastructure to be created. The generated code includes a provider block, comments, and the necessary infrastructure resources.

## Features

- Retrieves a Google API key from the environment.
- Generates Terraform code using the Generative AI model.
- Saves the generated Terraform code to a file.
- Optionally formats the generated code using Terraform's `terraform fmt` command.
- Customizable AWS region for the generated Terraform code.
- Retry logic for generating code with exponential backoff.

## Prerequisites

Before running the script, ensure you have the following installed:

1. **Python 3.7+**
2. **Terraform CLI** (to format the code with `terraform fmt`)
3. **Google Generative AI API access** (obtain an API key from Google)
4. **Python Dependencies**:
   - `google-generativeai` (for interacting with the Generative AI API)
   - `python-dotenv` (optional, for loading environment variables from a `.env` file)
   - `grpcio` (to fix issues related to gRPC)

To install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. **Set up the Google API Key:**
   
   You need a Google API key to interact with the Generative AI model. Set the API key as an environment variable:

   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

2. **Set up the environment for gRPC:**
   
   If you experience issues related to `epoll1` or other gRPC engine errors, you can adjust the environment variables:

   ```bash
   export GRPC_POLL_STRATEGY="select"  # Set to 'select' for better compatibility
   export GRPC_ENABLE_FORK_SUPPORT="0"
   ```

3. **Install Terraform** (if not already installed):

   You can install Terraform by following the instructions on the official website: https://www.terraform.io/downloads

4. **(Optional) Use a `.env` File:**

   You can store environment variables in a `.env` file to avoid setting them manually each time. Create a `.env` file and add the necessary environment variables:

   ```ini
   GOOGLE_API_KEY=your_api_key_here
   GRPC_POLL_STRATEGY=select
   GRPC_ENABLE_FORK_SUPPORT=0
   ```

   Then, load them in your script by adding the following lines:

   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Load environment variables from the .env file
   ```

## Usage

1. **Run the script**:

   You can run the script from the command line:

   ```bash
   python generate_terraform_code.py
   ```

2. **Input AWS Region** (Optional):
   
   You will be prompted to enter the AWS region for the Terraform provider. You can skip this and use the default region (`us-east-1`), or specify your own region.

3. **Generated Code**:
   
   The generated Terraform code will be saved in a file called `generated_infrastructure.tf`. If the file already exists, you will be prompted to overwrite it.

4. **Format the Terraform Code**:
   
   The script will automatically attempt to format the generated Terraform code using `terraform fmt`. Ensure that Terraform is installed and available in your PATH.

## Code Flow

1. **Retrieve API Key**: The `get_api_key` function retrieves the API key from the environment.
2. **Generate Terraform Code**: The `generate_terraform_code` function uses the Generative AI model to generate Terraform code based on a prompt.
3. **Save Terraform Code**: The `save_terraform_code` function saves the generated code to a file.
4. **Format Code**: The `format_terraform_code` function formats the generated code using Terraform’s `terraform fmt` command.
5. **Custom AWS Region**: The `get_aws_region_from_user` function allows the user to specify an AWS region.

## Example Prompt

The script uses a prompt to generate Terraform code. Here is an example of the prompt:

```plaintext
You are a helpful AI assistant that generates Terraform code for infrastructure deployment.
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
```

## Error Handling

- The script includes retry logic for API requests. If the first attempt fails, it will retry up to 3 times with exponential backoff.
- It will log errors if the Terraform CLI is not found or if there are issues with the generated code.

## Troubleshooting

1. **gRPC Errors**:
   If you encounter errors related to gRPC, try adjusting the `GRPC_POLL_STRATEGY` to `select` or removing it from the script entirely.

2. **Terraform Not Found**:
   If `terraform fmt` fails due to Terraform not being installed, you will see a warning. Install Terraform from [here](https://www.terraform.io/downloads).

3. **API Errors**:
   Ensure that the API key is valid and has the required permissions to interact with the Generative AI model.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to modify this README as necessary for your specific use case!
