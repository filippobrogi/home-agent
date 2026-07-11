
# HOME AGENT

This is my first AI project based on Ollama

## NVIDIA Container

```bash
docker info | grep -i runtime
```

when the output is

```bash
Runtimes: io.containerd.runc.v2 runc
Default Runtime: runc
```

then Docker does not have the NVIDIA container runtime installed/configured


1. First verify the host GPU works

Run 
```bash
nvidia-smi
```

You should see your GPU listed. If this fails, fix the Ubuntu NVIDIA driver first

2. Install NVIDIA Container Toolkit

On Ubuntu, install the toolki

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update

sudo apt install -y nvidia-container-toolkit

```

Then configure Docker:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

Restart Docker:

```bash
sudo systemctl restart docker
```

3. Verify Docker sees NVIDIA

Run again:

```bash
docker info | grep -i runtime
```

Expected:

```bash
Runtimes: io.containerd.runc.v2 nvidia runc
Default Runtime: runc
```

4. Test GPU inside a container

Before restarting Ollama, test:

```bash
docker run --rm --gpus all nvidia/cuda:12.6.0-base-ubuntu22.04 nvidia-smi
```

If successful, you should see the GPU from inside the container.