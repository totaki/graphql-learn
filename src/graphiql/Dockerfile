FROM node:8.2
RUN mkdir /srv/app
WORKDIR /srv/app
COPY . .

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb http://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install yarn \
    && mkdir /srv/app/static \
    && cd /srv/app \
    && yarn add graphiql --save \
    && yarn add express  --save \
    && curl https://cdn.jsdelivr.net/es6-promise/4.0.5/es6-promise.auto.min.js > /srv/app/static/es6-promise.auto.min.js \
    && curl https://cdn.jsdelivr.net/fetch/0.9.0/fetch.min.js > /srv/app/static/fetch.min.js \
    && curl https://cdn.jsdelivr.net/react/15.4.2/react.min.js > /srv/app/static/react.min.js \
    && curl https://cdn.jsdelivr.net/react/15.4.2/react-dom.min.js > /srv/app/static/react-dom.min.js

