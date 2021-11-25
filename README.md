# party*

Check out [http://cultofthepartyparrot.com/](http://cultofthepartyparrot.com/). The party parrot recently took over our Slack at [RainforestQA](https://www.rainforestqa.com/) and I thought that was not quite enough. Now, using **party**, you can make any image party with you!

## Running locally

```bash
docker build . -t partyasterisk && docker run --rm -it -p 5000:5000 --env DEBUG=1 partyasterisk gunicorn -b 0.0.0.0:5000 partyasterisk:app
```
