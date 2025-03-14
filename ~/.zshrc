# Source custom configurations
if [ -f "$HOME/.zshrc_custom" ]; then
    source "$HOME/.zshrc_custom"
fi

# Source pyenv control file
if [ -f "$HOME/.pyenv_control" ]; then
    source "$HOME/.pyenv_control"
fi

# Function to activate conda environment
activate_conda_env() {
    local env_name=$1
    if conda info --envs | grep -q "$env_name"; then
        conda activate "$env_name"
        echo "Activated conda environment: $env_name"
    else
        echo "Conda environment '$env_name' not found"
    fi
}

# Automatically activate new_env when opening a terminal
# Comment out the line below if you don't want this behavior
activate_conda_env "new_env"

# Alias for running the image analysis chatbot with the correct Python
alias run_chatbot='/opt/anaconda3/envs/new_env/bin/python /Users/mobin.azimipanah/Library/Mobile\ Documents/com~apple~CloudDocs/Desktop/Polimi/outlier/Image_AI_UI/image_analysis_chatbot.py'

# >>> conda initialize >>> 