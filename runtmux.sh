#/bin/bash
conda3
tmux kill-session -t landrov
tmux new-session -d -s landrov

tmux split-window -h
tmux select-pane -t 0
tmux send-keys "printf '\033]2;controler\033\\'" ENTER
tmux send-keys "python controler.py" ENTER


tmux select-pane -t 1
tmux send-keys "printf '\033]2;video_server.py\033\\'" ENTER
tmux send-keys "python video_server.py" ENTER


