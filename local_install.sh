#bin/bash
echo 'Please choose your favorite python environment manager!'
echo '1- Conda'
echo '2- Venv'
echo 'Enter 1 or 2:'
read envname

if [ $envname -eq 1 ]
then
    conda create -n qualiextra_env -c conda-forge python=3.11.6 --file requirements.txt -y
    echo '#bin/bash 
    conda activate qualiextra_env
    streamlit run Index.py --server.port=8501 --server.address=0.0.0.0
    ' > Qualiextra.sh
fi

if [ $envname -eq 2 ]
then
    python3 -m venv .qualiextra_env
    source .qualiextra_env/bin/activate
    pip install -r requirements.txt
    echo '#bin/bash 
    conda activate qualiextra_env
    streamlit run Index.py --server.port=8501 --server.address=0.0.0.0
    ' > Qualiextra.sh
fi

echo Installation done!
echo You can now launch the app using Qualiextra.sh