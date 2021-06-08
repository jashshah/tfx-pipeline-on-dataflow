FROM tensorflow/tfx:0.29.0
COPY ssl/* /usr/local/share/ca-certificates/
RUN update-ca-certificates
COPY ssl/pip.conf /etc/pip.conf
# RUN echo "ssl_verify: /etc/ssl/certs/ca-certificates.crt" >> /opt/conda/.condarc
RUN apt-get update && apt-get -y install git libsm6 libxext6 libxrender-dev libgl1-mesa-glx && apt-get clean
RUN apt-get update

# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN wget -nv \
    https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    rm -rf /root/tools && \
    mkdir /root/tools && \
    tar xvzf google-cloud-sdk.tar.gz -C /root/tools && \
    rm google-cloud-sdk.tar.gz && \
    /root/tools/google-cloud-sdk/install.sh --usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    rm -rf /root/.config/* && \
    ln -s /root/.config /config && \
    # Remove the backup directory that gcloud creates
    rm -rf /root/tools/google-cloud-sdk/.install/.backup
    
# Path configuration
ENV PATH $PATH:/root/tools/google-cloud-sdk/bin
# Make sure gsutil will use the default service account
RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg
# RUN pip install -r requirements.txt


RUN pip install google-cloud-storage
RUN pip install google-cloud-aiplatform
RUN pip install google-cloud-bigquery
RUN pip install fsspec
RUN pip install gcsfs
RUN pip install google-api-client
RUN pip install oauth2client
RUN pip install google-api-python-client
# RUN pip install tensorflow==2.4.1
# RUN pip uninstall apache-beam[gcp] -y
RUN pip install apache-beam[gcp]
# RUN pip install kfp==1.6.1

# RUN pip freeze | grep apache-beam
WORKDIR ./taxi_tfx

COPY ./ ./
RUN pwd   
RUN ls 
RUN pip install -r requirements.txt

ENV PYTHONPATH="/tfx_pipelines:${PYTHONPATH}"