import os
import shutil
import subprocess


def create_deployment_package():
    # Clean and create deployment directory
    if os.path.exists('deployment'):
        shutil.rmtree('deployment')
    os.makedirs('deployment')

    # Copy only the main package and lambda integration tests
    shutil.copytree(
        'src/birthday_wisher',
        'deployment/src/birthday_wisher',
        ignore=shutil.ignore_patterns(
            '__pycache__',
            '*.pyc'
        )
    )

    # Create test directory structure
    os.makedirs('deployment/src/test', exist_ok=True)

    # Copy only the lambda integration tests
    shutil.copytree(
        'src/test/lambdaintegrationtest',
        'deployment/src/test/lambdaintegrationtest',
        ignore=shutil.ignore_patterns(
            '__pycache__',
            '*.pyc'
        )
    )

    # Install only required dependencies (no test framework dependencies needed as unittest is built-in)
    subprocess.check_call([
        'pip',
        'install',
        '--platform',
        'manylinux2014_x86_64',
        '--target',
        'deployment',
        '--only-binary=:all:',
        'openai',
        'anthropic',
        'pydantic',
        'pydantic-core',
        'typing_extensions'
    ])

    # Remove unnecessary files
    patterns_to_remove = [
        '*.dist-info',
        '*.egg-info',
        '__pycache__',
        '*.pyc'
    ]

    for pattern in patterns_to_remove:
        for root, dirs, files in os.walk('deployment'):
            for item in dirs + files:
                if any(pattern.replace('*', '') in item for pattern in patterns_to_remove):
                    item_path = os.path.join(root, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)

    # Create the zip archive
    if os.path.exists('deployment-package.zip'):
        os.remove('deployment-package.zip')

    shutil.make_archive(
        'deployment-package',
        'zip',
        'deployment',
        verbose=True
    )

    # Print the size of the zip file
    zip_size = os.path.getsize('deployment-package.zip') / (1024 * 1024)  # Convert to MB
    print(f"\nDeployment package size: {zip_size:.2f} MB")


if __name__ == '__main__':
    create_deployment_package()