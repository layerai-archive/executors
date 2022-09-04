FROM tensorflow/tensorflow:2.8.0-gpu

# Replace old nvidia signing key with new one, and also old ones as well
# https://developer.nvidia.com/blog/updating-the-cuda-linux-gpg-repository-key/
RUN rm /etc/apt/sources.list.d/cuda.list \
    && rm /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-key del 7fa2af80 \
    && apt-get update && apt-get install -y --no-install-recommends git libgl1 \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub

COPY ./python-requirements/ /python-requirements/
RUN pip install --no-cache-dir \
    -r /python-requirements/vendor-requirements.txt \
    -r /python-requirements/vendor-requirements-gpu.txt \
    -r /python-requirements/requirements.txt \
    -f https://download.pytorch.org/whl/torch_stable.html \
  && rm -rf /python-requirements/

COPY ./entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]
