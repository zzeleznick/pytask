from datetime import datetime as dt
import re
# internals
from config import buildConfig

def build(zvals = []):
    ds = buildConfig(zvals)
    return ds

if __name__ == '__main__':
    pass