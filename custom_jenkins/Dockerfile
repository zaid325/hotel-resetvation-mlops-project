# Use the official Jenkins LTS image as base
FROM jenkins/jenkins:lts

# Switch to root to install dependencies
USER root

# Install Docker Engine inside Jenkins container
RUN apt-get update -y && \
    apt-get install -y ca-certificates curl gnupg lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Jenkins user to the Docker group
RUN groupadd -f docker && usermod -aG docker jenkins

# Create a Docker volume for DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to Jenkins user
USER jenkins






