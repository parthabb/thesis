if [[ -f .venv/bin/activate ]]; then
    echo "Start virtual environment"
    . .venv/bin/activate
    export PYTHONPATH=$PYTHONPATH:./lib
fi
