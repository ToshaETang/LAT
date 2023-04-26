'use strict';
const express = require('express'),
      configGet = require('config');
const {TextAnalyticsClient, AzureKeyCredential} = require("@azure/ai-text-analytics");

//Azure Text Sentiment
const endpoint = configGet.get("ENDPOINT");
const apiKey = configGet.get("TEXT_ANALYTICS_API_KEY");

const app = express();

const port = process.env.PORT || process.env.port || 3001;

app.listen(port, ()=>{
  console.log(`listening on ${port}`);
  MS_TextSentimentAnalysis()
  .catch((err)=>{
    console.error("Error:",err);
  });  
});

async function MS_TextSentimentAnalysis(){
    console.log("[MS_TextSentimentAnalysis] in");
    const analyticsClient = new TextAnalyticsClient(endpoint, new AzureKeyCredential(apiKey));
    let documents = [];
    documents.push("我覺得櫃檯人員很親切");
    const results = await analyticsClient.analyzeSentiment(documents);
    console.log("[results] ", JSON.stringify(results));
}