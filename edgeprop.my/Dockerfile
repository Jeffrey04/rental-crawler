FROM jonatkinson/python-poetry:3.7

COPY docker/opt/crawler /opt/crawler

WORKDIR /opt/crawler

RUN mkdir -p /var/lib/crawler && \
    touch /var/lib/crawler/crawler.db && \
    chmod o+w /var/lib/crawler/crawler.db && \
    sync && \
    poetry install --no-dev

VOLUME /var/lib/crawler

CMD ["poetry", "run", "python", "bin/crawler.py"]