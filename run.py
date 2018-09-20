#!/usr/bin/env python3
from routes import app, ems
    
if __name__ == '__main__':
    # start web server  
    app.run()
    
    # dump data before exiting
    print()
    ems.dumpData()
    print("Exiting...")
