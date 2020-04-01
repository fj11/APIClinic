
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function httpGet(url){
    return $.ajax({
        url: url,
        method: "GET",
        headers:{
            "X-CSRFTOken": getCookie('csrftoken')
                }
    })

}

function httpPost(url, content){

    return $.ajax({
        url: url,
        method: "POST",
        data: content,
        headers:{
            "X-CSRFTOken": getCookie('csrftoken')
                }
    })

}

function testResultListItems(testResults){
    for (i=testResults.length-1;i>0;i--){

        testResult = testResults[i];
        item = "<a href='#' class='list-group-item d-flex justify-content-between align-items-center' id=" + testResult["id"] + ">Test Result";

        if (testResult["failed_number"] > 0){
            item += "<span class='badge badge-danger badge-pill'>" + testResult["failed_number"] + "</span>";
        }
        // item += "<span class='badge badge-primary badge-pill'>" + testResult["pass_number"] + "</span>"
        item += "</a>";
        $("#test_result_list_group").append(item);
    }
}


$( document ).ready(function() {
    testResults = httpGet("/restapi/testresult/");
    testResults.done(function(data){
        testResultListItems(data);
        $("#test_result_list_group a").click(function() {
            url = "/restapi/testresult/?id=" + $(this).attr("id");
            var testResult = httpGet(url);
            testResult.done(function(data){
                console.log(data);
                $("#head_display").text(data["name"]);
                $("#start_time_display").text(data["start_time"]);
                $("#end_time_display").text(data["end_time"]);
                $("#duration_time_display").text(data["duration"]);
            })
          });
    })
    
});

