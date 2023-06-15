FROM tensorflow/tensorflow
WORKDIR /app
ENV FLASK_APP=GenAPI.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV api_key=989b884e-99ac-4caf-9417-f3528274e391
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 5000
COPY . .
CMD ["flask", "run"]