import sys

def verify_dependencies():
    required_packages = [
        'PyQt6',
        'ping3',
        'requests',
        'scapy',
        'psutil'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} successfully imported")
        except ImportError as e:
            missing_packages.append(package)
            print(f"✗ Failed to import {package}: {str(e)}")
    
    if missing_packages:
        print("\nMissing packages:", ", ".join(missing_packages))
        sys.exit(1)
    else:
        print("\nAll dependencies verified successfully!")

if __name__ == "__main__":
    verify_dependencies()
