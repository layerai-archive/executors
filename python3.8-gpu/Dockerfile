FROM tensorflow/tensorflow:2.8.0-gpu

# Replace old nvidia signing key with new one, and also old ones as well
# https://developer.nvidia.com/blog/updating-the-cuda-linux-gpg-repository-key/
RUN rm /etc/apt/sources.list.d/cuda.list \
    && rm /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-key del 7fa2af80 \
    && apt-get update && apt-get install -y --no-install-recommends git libgl1 \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub

COPY ml-requirements.txt ./ml-requirements.txt
RUN pip install --no-cache-dir -r /ml-requirements.txt -f https://download.pytorch.org/whl/torch_stable.html \
    && rm -f ./ml-requirements.txt

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -f ./requirements.txt

ENTRYPOINT ["python", "-m", "layer.executables.runtime"]
