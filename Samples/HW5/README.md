<p>構想: 透過輸入主體明顯且背景簡單的圖片，可得到該物體的英文單字，適合用於情境式英語學習</p>


<p>主要更動: 改成顯示tags</p>

```
//顯示JSON內容
        $("#responseTextArea").val(JSON.stringify(data, null, 2));
        $("#picDescription").empty();
        for (var x = 0; x < data.description.tags.length;x++){
            $("#picDescription").append(data.description.tags[x] + "<br>");
        }
```

![圖片](https://github.com/ToshaETang/LAT/blob/main/Samples/HW5/apple.jpg "結果")  
![圖片](https://github.com/ToshaETang/LAT/blob/main/Samples/HW5/car.jpg "結果")  
![圖片](https://github.com/ToshaETang/LAT/blob/main/Samples/HW5/hat.jpg "結果")  
![圖片](https://github.com/ToshaETang/LAT/blob/main/Samples/HW5/banana.jpg "結果")  


<p>source code</p>

```
$(document).ready(function(){
    //do something
    $("#thisButton").click(function(){
        processImage();
    });
    $("#inputImageFile").change(function(e){
        processImageFile(e.target.files[0]);
    });
});

function processImage() {
    
    //確認區域與所選擇的相同或使用客製化端點網址
    var url = "https://eastus.api.cognitive.microsoft.com/";
    var uriBase = url + "vision/v2.1/describe";
    
    var params = {
        //"visualFeatures": "Faces,Objects,Adult,Brands,Categories,Description",
        // "details": "Landmarks",
        "maxCandidates":"3",
        "language": "en",
    };
    //顯示分析的圖片
    var sourceImageUrl = document.getElementById("inputImage").value;
    document.querySelector("#sourceImage").src = sourceImageUrl;
    //送出分析
    $.ajax({
        url: uriBase + "?" + $.param(params),
        // Request header
        beforeSend: function(xhrObj){
            xhrObj.setRequestHeader("Content-Type","application/json");
            xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
        },
        type: "POST",
        // Request body
        data: '{"url": ' + '"' + sourceImageUrl + '"}',
    })
    .done(function(data) {
        //顯示JSON內容
        $("#responseTextArea").val(JSON.stringify(data, null, 2));
        $("#picDescription").empty();
        for (var x = 0; x < data.description.tags.length;x++){
            $("#picDescription").append(data.description.tags[x] + "<br>");
        }
        // $("#picDescription").append("這裡有"+data.faces.length+"個人");
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        //丟出錯誤訊息
        var errorString = (errorThrown === "") ? "Error. " : errorThrown + " (" + jqXHR.status + "): ";
        errorString += (jqXHR.responseText === "") ? "" : jQuery.parseJSON(jqXHR.responseText).message;
        alert(errorString);
    });
};//



function processImageFile(imageObject) {
    
    //確認區域與所選擇的相同或使用客製化端點網址
    var url = "https://eastus.api.cognitive.microsoft.com/";
    var uriBase = url + "vision/v2.1/describe";
    
    var params = {
        "visualFeatures": "Faces,Objects,Adult,Brands,Categories,Description",
        // "details": "Landmarks",
        "maxCandidates":"10",
        "language": "en",
    };
    //顯示分析的圖片
    var sourceImageUrl = URL.createObjectURL(imageObject);
    document.querySelector("#sourceImage").src = sourceImageUrl;
    //送出分析
    $.ajax({
        url: uriBase + "?" + $.param(params),
        // Request header
        beforeSend: function(xhrObj){
            xhrObj.setRequestHeader("Content-Type","application/octet-stream");
            xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
        },
        type: "POST",
        processData:false,
        contentType:false,
        // Request body
        data: imageObject,
    })
    .done(function(data) {
        //顯示JSON內容
        $("#responseTextArea").val(JSON.stringify(data, null, 2));
        $("#picDescription").empty();
        for (var x = 0; x < data.description.tags.length;x++){
            $("#picDescription").append(data.description.tags[x] + "<br>");
        }
        // $("#picDescription").append("這裡有"+data.faces.length+"個人");
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        //丟出錯誤訊息
        var errorString = (errorThrown === "") ? "Error. " : errorThrown + " (" + jqXHR.status + "): ";
        errorString += (jqXHR.responseText === "") ? "" : jQuery.parseJSON(jqXHR.responseText).message;
        alert(errorString);
    });
};//
```


