Here's the command to copy the corrected file:

```bash
sudo cp /home/diogenes/projects/github.com/harder-video-drives/exp/sources-list-fix/etc/apt/sources.list.d/microsoft-edge.list /etc/apt/sources.list.d/microsoft-edge.list
```

Or from the `exp/sources-list-fix` directory:

```bash
sudo cp etc/apt/sources.list.d/microsoft-edge.list /etc/apt/sources.list.d/microsoft-edge.list
```

After copying, run `sudo apt update` to verify the warnings are gone.
