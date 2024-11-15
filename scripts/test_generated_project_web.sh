#!/bin/bash
set -e  # Exit on error

if [ ! -d "test-output/test_app" ]; then
    echo "Error: Test project not found. Please run ./scripts/generate_test_project_from_template.sh first"
    exit 1
fi

cd test-output/test_app

echo "Testing web interface..."
source venvg/bin/activate

# Start the web server in the background
python -m test_app.__web__ &
WEB_PID=$!

echo "Waiting for server to start..."
sleep 2

# Test that the server is responding
if curl -s http://localhost:8080/ > /dev/null; then
    echo "Web server is running at http://localhost:8080"
else
    echo "Error: Web server is not responding"
    kill $WEB_PID
    exit 1
fi

# Give user time to check the website
echo "Website is available for testing at http://localhost:8080"
echo "Press Enter to stop the server..."
read

# Cleanup
kill $WEB_PID
deactivate
cd ../..

echo "Web test completed successfully!"
