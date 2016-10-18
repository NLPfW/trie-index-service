# Docker image for the trie index service
#

FROM python:2-onbuild
EXPOSE 9528
CMD [ "python", "./src/app.py" ]
