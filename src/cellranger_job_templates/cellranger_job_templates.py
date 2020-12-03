"""Main module."""
#!/usr/bin/env python
import os
import pwd


def get_userhome() -> str:
    return pwd.getpwuid(os.getuid()).pw_dir
