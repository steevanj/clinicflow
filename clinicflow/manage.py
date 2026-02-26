#!/usr/bin/env python
import os
import sys


def main():
    settings_module = os.getenv(
        "DJANGO_SETTINGS_MODULE",
        "clinicflow.settings.development"
    )

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()