# Docker Conda environment with heavydb libs

## Build docker
```bash
docker build -t "mm_conda_heavydb_img" .
```

## Run docker
```bash
./start_conda.bash
```
And then inside docker
```bash
conda activate heavyai
cd /root/scripts
python {selected_file.py}
```
