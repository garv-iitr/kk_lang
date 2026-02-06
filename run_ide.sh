
cleanup() {
    echo "Stopping KhelKhatam Server..."
    kill $FLASK_PID
    exit
}

trap cleanup SIGINT

echo "--------------------------------"

echo "Checking dependencies..."
pip3 install flask flask-cors flask-limiter > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing Flask-Limiter..."
    pip3 install Flask-Limiter
fi

echo "Cleaning up port 5000..."
lsof -ti:5000 | xargs kill -9 2>/dev/null
sleep 1

echo "Building Sandbox Docker Image..."
if ! docker build -t khelkhatam-runner .; then
    echo "Docker build failed! Aborting."
    exit 1
fi
echo "Docker Image 'khelkhatam-runner' built successfully."


echo "Starting Flask Server (Port 5000)..."
python3 app.py &
FLASK_PID=$!
sleep 2 

echo "Opening IDE in Browser..."
if command -v open &> /dev/null; then
    open http://localhost:5000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000
else
    echo "Please open: http://localhost:5000"
fi

echo "--------------------------------"
echo "Server Running on http://localhost:5000"
echo "Press Ctrl+C to stop."
echo "--------------------------------"

wait