FROM python:3

# Force Redeploy
ADD https://api.github.com/repos/shreyasgokhale/junction_2019_slingshot/git/refs/heads/master master.json
# RUN apk --update add bash nano
# ENV STATIC_URL /static
# ENV STATIC_PATH /var/www/app/static
# COPY ./requirements.txt /var/www/requirements.txt
COPY ./src /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "/app/main.py" ]
