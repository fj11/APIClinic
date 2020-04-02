
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
$('#test_result_list_group a').on('click', function (e) {
    url = "/restapi/testresult/?id=" + $(this).attr("id");
    var testResult = httpGet(url);
    testResult.done(function(data){
        $('#test_case_detail_list').remove();
        $("#head_display").text(data["name"]);
        $("#start_time_display").text(data["start_time"]);
        $("#end_time_display").text(data["end_time"]);
        $("#duration_time_display").text(data["duration"]);
        updateTestCaseResultList(data["details"]);
    })

});

function updateTestCaseResultList(testCaseResults){
    listGroup = "<div id='test_case_detail_list' class='list-group'>"
    for (i=0;i<testCaseResults.length;i++){
        testCaseResult = testCaseResults[i];
        if (testCaseResult['result'] == "PASS"){
            listGroup += "<a href='#' class='list-group-item list-group-item-action list-group-item-primary'>" + testCaseResult["testcase"]['name'] + "</a>";

        }
        else{
            listGroup += "<a href='#' class='list-group-item list-group-item-action list-group-item-danger'>"+ testCaseResult["testcase"]['name'] +"</a>";
        }
        
    }
    listGroup += "</div>"
    $('#detail_display').append(listGroup);

}

