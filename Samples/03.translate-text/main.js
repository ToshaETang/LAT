$(document).ready(function(){
    //do something
    $("#thisButton").click(function(){
        processTranslate();
    });
});

function processTranslate() {
    
    let uriBase = "https://api.cognitive.microsofttranslator.com/translate";
    let params = {
        "api-version": "3.0",
        "to": "zh-Hant,th,en,ja"
    };
    //取得要翻譯的文字
    let sourceTranslateText = document.getElementById("inputText").value;
    
    //送出分析
    $.ajax({
        url: uriBase + "?" + $.param(params),
        // Request header
        beforeSend: function(xhrObj){
            xhrObj.setRequestHeader("Content-Type","application/json");
            xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
            // 如果不是設定全域，就要加上這一行指定你所選擇的區域
            xhrObj.setRequestHeader("Ocp-Apim-Subscription-Region", "eastus");
        },
        type: "POST",
        // Request body
        data: '[{"Text": ' + '"' + sourceTranslateText + '"}]',
    })
    .done(function(data) {
        //顯示JSON內容
        $("#translateResult").empty();
        $("#responseTextArea").val(JSON.stringify(data, null, 2));
        //修改下面這一行將翻譯結果顯示於右方
        for(var x=0; x<data[0].translations.length;x++){
            $("#translateResult").append(data[0].translations[x].text+"<br>");
        }


        //$("#translateResult").text(data[0].translations[0].text);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        //丟出錯誤訊息
        var errorString = (errorThrown === "") ? "Error. " : errorThrown + " (" + jqXHR.status + "): ";
        errorString += (jqXHR.responseText === "") ? "" : jQuery.parseJSON(jqXHR.responseText).message;
        alert(errorString);
    });
};