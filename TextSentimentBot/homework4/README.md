<p>Here is my source code</p>

```
'use strict';
const line = require('@line/bot-sdk'),
      express = require('express'),
      configGet = require('config');
const {TextAnalyticsClient, AzureKeyCredential} = require("@azure/ai-text-analytics");

//Line config
const configLine = {
  channelAccessToken:configGet.get("CHANNEL_ACCESS_TOKEN"),
  channelSecret:configGet.get("CHANNEL_SECRET")
};

//Azure Text Sentiment
const endpoint = configGet.get("ENDPOINT");
const apiKey = configGet.get("TEXT_ANALYTICS_API_KEY");

const client = new line.Client(configLine);
const app = express();

const port = process.env.PORT || process.env.port || 3001;
app.listen(port, ()=>{
  console.log(`listening on ${port}`);   
});

async function MS_TextSentimentAnalysis(thisEvent){
    console.log("[MS_TextSentimentAnalysis] in");
    const analyticsClient = new TextAnalyticsClient(endpoint, new AzureKeyCredential(apiKey));
    let documents = [];
    documents.push(thisEvent.message.text);
  
    const results = await analyticsClient.analyzeSentiment(documents,"zh-Hant",{includeOpinionMining: true});
    console.log("[results] ", JSON.stringify(results));

    if(results[0].sentiment == "positive"){
      const echo = {
        type: 'text',
        text: "正面" + "  confidenceScores=" +results[0].confidenceScores[results[0].sentiment.toLowerCase()]
      };
      return client.replyMessage(thisEvent.replyToken, echo);
    }
    else if(results[0].sentiment == "negative"){
      const echo = {
        type: 'text',
        text: "負面" + "  confidenceScores=" +results[0].confidenceScores[results[0].sentiment.toLowerCase()]
      };
      return client.replyMessage(thisEvent.replyToken, echo);
    }
    else{
      const echo = {
        type: 'text',
        text: "中性" + "  confidenceScores=" +results[0].confidenceScores[results[0].sentiment.toLowerCase()]
      };
      return client.replyMessage(thisEvent.replyToken, echo);
    }
}

app.post('/callback', line.middleware(configLine),(req, res)=>{
  Promise
    .all(req.body.events.map(handleEvent))
    .then((result)=>res.json(result))
    .catch((err)=>{
      console.error(err);
      res.status(500).end();
    });
});

function handleEvent(event){
  if(event.type !== 'message' || event.message.type !== 'text'){
    return Promise.resolve(null);
  }
  MS_TextSentimentAnalysis(event)
    .catch((err) => {
      console.error("Error:", err);
    }); 
}
```

<p>Here is my result</p>
![圖片](https://github.com/ToshaETang/LAT/blob/main/TextSentimentBot/homework4/resultImage.jpg "結果")
