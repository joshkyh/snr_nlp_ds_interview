# Basic setup
FROM python:3.10-slim-bookworm

# add git lhs to apt
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash

# Update and install necessary packages
RUN apt-get update && apt-get -y update
# added vim and nano for convenience
RUN apt-get install -y sudo git nano curl wget git-lfs libmagic1


# Clone the AutoGen repository
WORKDIR /home/snr_nlp_ds_interview

# Set the default command to bash
CMD ["/bin/bash"]
