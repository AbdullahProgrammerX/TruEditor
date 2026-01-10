#!/usr/bin/env bash
# ============================================
# TruEditor - Render Build Script
# ============================================
# Bu script Render.com tarafından deployment sırasında çalıştırılır.

set -o errexit  # Hata durumunda script'i durdur

echo ">>> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements/production.txt

echo ">>> Creating logs directory..."
mkdir -p logs

echo ">>> Collecting static files..."
python manage.py collectstatic --no-input

echo ">>> Running database migrations..."
python manage.py migrate --no-input

echo ">>> Build completed successfully!"
