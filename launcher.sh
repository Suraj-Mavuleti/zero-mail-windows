#!/bin/bash
# AUTO-UPDATER
cd /home/suraj/.gemini/antigravity/scratch/zero_suite/zero-mail-windows
git pull origin main --quiet
python3 zero_mail_gui.py
