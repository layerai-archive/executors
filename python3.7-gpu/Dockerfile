FROM tensorflow/tensorflow:2.8.0-gpu

# Replace old nvidia signing key with new one, and also old ones as well
# https://developer.nvidia.com/blog/updating-the-cuda-linux-gpg-repository-key/
RUN rm /etc/apt/sources.list.d/cuda.list \
    && rm /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-key del 7fa2af80 \
    && apt-get update && apt-get install -y --no-install-recommends wget git libgl1 \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub

# python3.8 is default for ubuntu 20:04 so we need to add additional repo for older releases
RUN add-apt-repository ppa:deadsnakes/ppa \
    #remove packages and preinstalled python 3.8 itself
    && pip freeze | xargs pip uninstall -y \
    && apt-get remove --purge --auto-remove -y python3-pip python3

#install 3.7 and fix symlinks
RUN apt-get install -y --no-install-recommends python3.7 python3.7-distutils \
    && curl https://bootstrap.pypa.io/get-pip.py | python3.7 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

COPY ml-requirements.txt ./ml-requirements.txt
RUN pip install --no-cache-dir -r /ml-requirements.txt -f https://download.pytorch.org/whl/torch_stable.html \
    && rm -f ./ml-requirements.txt

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -f ./requirements.txt

ENTRYPOINT ["python", "-m", "layer.executables.runtime"]
