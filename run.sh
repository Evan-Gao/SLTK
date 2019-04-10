# preprocessing and train
#CUDA_VISIBLE_DEVICES=0 python3 -u main.py --config ./configs/squad.yml -p --train

# train only
CUDA_VISIBLE_DEVICES=1 python3 -u main.py --config ./configs/squad.yml --train

# test
#CUDA_VISIBLE_DEVICES=0 python3 main.py --config ./configs/squad.yml --test