<p>Here is my source code</p>

```
'use strict';
const line = require('@line/bot-sdk'),
      express = require('express'),
      axios = require('axios'),
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
    // documents.push("我覺得櫃檯人員很親切");
    // documents.push("熱水都不熱，爛死了，很生氣！");
    // documents.push("房間陳設一般般");
    const results = await analyticsClient.analyzeSentiment(documents,'zh-Hant',{
      includeOpinionMining:true
    });
    console.log("[results] ", JSON.stringify(results));
    //Save to JSON Server
    let newData = {
      "sentiment": results[0].sentiment,
      "confidenceScore": results[0].confidenceScores[results[0].sentiment],
      "opinionText":""
    };

    if(results[0].sentences[0].opinions.length!=0){
      newData.opinionText = results[0].sentences[0].opinions[0].target.text;
    }

    let axios_add_data = {
      method:"post",
      url:"https://toshaelsatanglathw4.azurewebsites.net/reviews",
      headers:{
        "content-type":"application/json"
      },
      data:newData
    };

    axios(axios_add_data)
    .then(function(response){
      console.log(JSON.stringify(response.data));
    })
    .catch(function(){
      console.log("Error!!");
    });

    const echo = {
      type: 'text',
      text: results[0].sentiment
    };
    return client.replyMessage(thisEvent.replyToken, echo);


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

```
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title></title>
        <link rel="stylesheet"href="">
    </head>
    <body>
        <div id="myDiv"></div>
        <script src="//unpkg.com/jquery"></script>
        <script src="https://cdn.plot.ly/plotly-2.20.0.min.js" charset="utf-8"></script>
        <script src="main.js"></script>
    </body>
</html>
```

```
let data = [{
    values:[1,1,1],
    labels:['Negative','Neutral','Positive'],
    type:'pie'
}];

let layout = {
    height:500,
    width:500
};

$(function(){
    // setInterval(readData,5000);
    readData();
});

function readData(){
    //Read data
    let url = "https://toshaelsatanglathw4.azurewebsites.net/reviews";
    $.getJSON(url)
     .done(function(msg){
        console.log(msg);
        data[0].values[0] = 0;
        data[0].values[1] = 0;
        data[0].values[2] = 0;
        let sentiments = ['negative','neutral','positive'];
        for(let x=0; x<msg.length;x++){
            for(let y=0;y<sentiments.length;y++){
                if(msg[x].sentiment == sentiments[y]){
                    data[0].values[y] += 1;
                }
            }
        }
         Plotly.newPlot("myDiv", data, layout);
     })
     .fail(function(msg){console.log("Fail");});
}
```
<p>I can't install Live Server so there is no result picture</p>
