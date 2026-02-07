# Base Spark image (stable & widely used)
FROM apache/spark:3.5.8-scala2.12-java11-python3-r-ubuntu

# Switch to root for system-level installs
USER root

# Install OS dependencies and Python tooling
RUN apt-get update && \
    apt-get install -y \
        python3-pip \
        python3-dev \
        build-essential \
        vim \
        nano \
        bash-completion && \
    pip3 install \
        jupyterlab \
        numpy \
        pandas \
        pyarrow \
        fastparquet \
        ipython && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo ". /usr/share/bash-completion/bash_completion" >> /etc/bash.bashrc

# Explicitly bind Spark to Python 3 (critical for clusters)
# Spark + Python binding
ENV SPARK_HOME=/opt/spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip


# Prepare Jupyter runtime and workspace directories
RUN mkdir -p \
        /home/spark/.local/share/jupyter/runtime \
        /opt/spark-app && \
    chown -R spark:spark \
        /home/spark \
        /opt/spark-app

# Drop root privileges (best practice)
USER spark
ENV HOME=/home/spark
ENV SHELL=/bin/bash

# Default working directory (mapped to ./app from host)
WORKDIR /opt/spark-app

# Expose Jupyter and Spark Driver UI ports
EXPOSE 8888 4040

# Start JupyterLab on container startup
CMD ["python3", "-m", "jupyterlab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
