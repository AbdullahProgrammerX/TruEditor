#!/usr/bin/env bash
# ============================================
# TruEditor - Render Build Script
# ============================================
# Bu script Render.com tarafından deployment sırasında çalıştırılır.

set -o errexit  # Hata durumunda script'i durdur

echo "============================================"
echo ">>> TruEditor Build Started"
echo "============================================"

echo ">>> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements/production.txt

echo ">>> Creating logs directory..."
mkdir -p logs

echo ">>> Collecting static files..."
python manage.py collectstatic --no-input

echo "============================================"
echo ">>> Running database migrations..."
echo "============================================"

# Show migration status first
echo ">>> Checking migration status..."
python manage.py showmigrations

# Run migrations with verbosity
echo ">>> Applying migrations..."
python manage.py migrate --no-input --verbosity 2

# Verify migrations applied
echo ">>> Verifying migrations..."
python manage.py showmigrations

echo "============================================"
echo ">>> Build completed successfully!"
echo "============================================"
