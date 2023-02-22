# Requirements
- python-i3ipc

# Simple master stack
Toggles between vertical and horizontal splitting  
### Usage
```
exec_always --no-startup-id {path_to_i3utils}/i3masterstack.py
```

# Swap
Swaps the focused workspace with the next visible workspace (Swap monitors)  
### Usage 
```
bindsym $mod+Shift+s exec {path_to_i3_utils}/i3swap.py
```

# Next workspace
Go to next available workspace  
-m for moving the focused container to the next workspace  
### Usage
```
bindsym $mod+grave exec {path_to_i3_utils}/i3nextworkspace.py
bindsym $mod+Shift+grave exec {path_to_i3_utils}/i3nextworkspace.py -m
```
