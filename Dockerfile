FROM --platform=linux/amd64 ubuntu:latest

# Update Ubuntu packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Install Miniconda
RUN apt-get install -y curl && \
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh



# Set Conda path
ENV PATH="/opt/conda/bin:${PATH}"

# Copy environment file
COPY environment.yml /tmp/environment.yml
RUN conda install mamba -c conda-forge
# Create Conda environment from environment file
RUN mamba env create --name cellsnake --file /tmp/environment.yml && \
    rm /tmp/environment.yml

# Activate Conda environment and install a package from PyPI
SHELL ["bash", "-c"]
RUN source activate cellsnake && \
    pip install cellsnake==0.2.0.11

#RUN source activate cellsnake && cellsnake --install-packages
COPY workflow/scripts/scrna-install-packages.R /tmp/scrna-install-packages.R 
RUN source activate cellsnake && Rscript /tmp/scrna-install-packages.R
# Set working directory
WORKDIR /app

# Start bash shell
ENTRYPOINT ["bash", "-c", "source activate cellsnake && exec $0 $@"]

CMD ["cellsnake --help"]
