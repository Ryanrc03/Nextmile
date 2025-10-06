#!/bin/sh
set -e

# Export environment variables to make them available to Node.js
export EMAIL_USER="${EMAIL_USER}"
export EMAIL_PASS="${EMAIL_PASS}"
export NODE_ENV="${NODE_ENV:-production}"

# Print environment variables for debugging (without sensitive values)
echo "Starting Next.js application..."
echo "NODE_ENV: ${NODE_ENV}"
echo "EMAIL_USER: $([ -n "$EMAIL_USER" ] && echo 'SET' || echo 'NOT SET')"
echo "EMAIL_PASS: $([ -n "$EMAIL_PASS" ] && echo 'SET' || echo 'NOT SET')"

# Start the application
exec node server.js
