#!/bin/bash
# tar -xzf /mnt/letsencrypt/etc.tar.gz -C / &&
nginx -t &&
service nginx start &&
# cron &&
streamlit run app/app.py --theme.base "light"
