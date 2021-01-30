FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev npm nodejs
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 5000
EXPOSE 8080
COPY . .
CMD ["npx", "nodemon", "--exec", "python3 -u -m", "bot.main"]