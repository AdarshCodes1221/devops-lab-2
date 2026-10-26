# OTT Video Streaming Microservice - Video Transcoder Engine
FROM alpine:3.20

# Install python3 and curl for health probes
RUN apk add --no-cache python3 curl

WORKDIR /app

# Copy application code and transcoding profile
COPY app.py /app/app.py
COPY transcode.conf /app/transcode.conf

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=80

EXPOSE 80

# When the container launches, it executes the transcoder engine printing "transcoder engine ready"
CMD ["python3", "-u", "/app/app.py"]
