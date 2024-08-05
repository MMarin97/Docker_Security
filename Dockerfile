# Stage 1: Build the application
FROM python:3.9-slim AS build
WORKDIR /MMarin_Test
RUN apt-get update && \
    apt-get install -y binutils && \
    pip install pyinstaller && \
    pip install fastapi && \
    pip install uvicorn && \
    pip install paho-mqtt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY . .
RUN pyinstaller --onefile main.py

# Stage 2: Create a minimal image with the compiled binary
FROM python:3.9-slim
WORKDIR /MMarin_Test
COPY --from=build /MMarin_Test/dist/main /MMarin_Test/main
CMD ["./main"]