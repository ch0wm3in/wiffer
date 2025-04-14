#!/bin/bash
exec gunicorn -w 4 -b :5000 --preload --access-logfile - --error-logfile - 'src.app:app'