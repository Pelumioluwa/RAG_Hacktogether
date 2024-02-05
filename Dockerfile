FROM mambaorg/micromamba:0.15.3
USER root
RUN apt-get update && DEBIAN_FRONTEND=“noninteractive” apt-get install -y --no-install-recommends \
        nginx \
        ca-certificates \
        apache2-utils \
        certbot \
        python3-certbot-nginx \
        sudo \
        cifs-utils \
        && \
     rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get -y install cron
RUN mkdir /opt/hackapp_azure
RUN chmod -R 777 /opt/hackapp_azure
WORKDIR /opt/hackapp_azure
USER micromamba
COPY environment.yml environment.yml
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
COPY run.sh run.sh
COPY app app
COPY nginx.conf /etc/nginx/nginx.conf
USER root
# RUN touch /var/log/cron.log
# # Setup cron job
# RUN (crontab -l ; echo "0 12 * * * /usr/bin/certbot renew --quiet && tar -cpzf /mnt/letsencrypt/etc.tar.gz -C / etc/letsencrypt/ ") | crontab
RUN chmod a+x run.sh
CMD ["./run.sh"]

## V1
# FROM mambaorg/micromamba:0.15.3
# USER root
# RUN mkdir /opt/hackapp_azure
# RUN chmod -R 777 /opt/hackapp_azure
# WORKDIR /opt/hackapp_azure
# USER micromamba
# COPY environment.yml environment.yml
# RUN micromamba install -y -n base -f environment.yml && \
#    micromamba clean --all --yes
# COPY run.sh run.sh
# COPY app app
# USER root
# RUN chmod a+x run.sh
# CMD ["./run.sh"]
