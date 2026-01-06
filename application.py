import uvicorn
import argparse
from config import settings

"""
    Application Entry Point: from here the service is started setting a specific port and host
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI paramaters to manage Video Rag')
    parser.add_argument(
        '-host',
        dest='host',
        default=settings.IP,
        type=str,
        action='store',
        help='API host address')
    parser.add_argument(
        '-port',
        dest='port',
        default=settings.PORT,
        type=int,
        action='store',
        help='API service port number')
    args = parser.parse_args()
    uvicorn.run('app:app', port=args.port, host=args.host)