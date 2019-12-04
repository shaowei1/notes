```
FROM python:3
COPY ./app /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.pip
CMD ["python","start.py","(api-url) ","(api-key)","(file-path)"]
Note Per each args/params, separate with coma

If you are using flags, you will need to split

CMD ["python","start.py","-u","(api-url) ","-k","(api-key)","-f","(file-path)"]
```
