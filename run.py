import os
import sys
from daphne.cli import CommandLineInterface

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VehicleDetection.settings')
    
    sys.argv = [
        'daphne',
        '-b', '0.0.0.0',
        '-p', '8500',
        'VehicleDetection.asgi:application'
    ]
    
    CommandLineInterface.entrypoint()

if __name__ == '__main__':
    main()
    