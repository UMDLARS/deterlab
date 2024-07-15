FROM wernight/phantomjs

# Set the working directory
WORKDIR /docker

# Copy the script to the working directory
COPY section_2.js .

# Switch to root, then add a user.
USER root
RUN adduser --disabled-password --gecos '' docker_user && \
    chown -R docker_user:docker_user /docker

# Create the /output directory and set permissions.
# This is for outputting responses to the /home/.checker directory.
RUN mkdir -p /output && \
    chown -R docker_user:docker_user /output && \
    chmod 777 /docker

# Switch to the new user for running the script.
USER docker_user

ENTRYPOINT ["phantomjs", "section_2.js"]
CMD ["<step_num>"]
