FROM python:alpine3.8
WORKDIR /opt/
COPY ./ ./
RUN mkdir .pip && cd .pip && echo -e "[global]\ntimeout = 60\nindex-url = http://pypi.douban.com/simple\ntrusted-host = pypi.douban.com\n" | tee pip.conf
RUN pip install --upgrade pip
RUN pip install --user -r requirements.txt
# RUN export FLASK_APP=feishu-alert.py
CMD ["python","feishu-alert.py"]