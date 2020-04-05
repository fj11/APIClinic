$(document).ready(function(){
    $("#test_result_list_group a:first").click();
    
})

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
    });

});

function updateTestCaseResultList(testCaseResults){
    listGroup = "<div id='test_case_detail_list' class='list-group'>"
    for (i=0;i<testCaseResults.length;i++){
        testCaseResult = testCaseResults[i];
        if (testCaseResult['result'] == "PASS"){
            listGroup += "<a href='#' id=" + testCaseResult["id"] + " class='list-group-item list-group-item-action list-group-item-primary'>" + testCaseResult["testcase"]['name'] + "</a>";
        }
        else{
            listGroup += "<a href='#' id=" + testCaseResult["id"] + " class='list-group-item list-group-item-action list-group-item-danger'>"+ testCaseResult["testcase"]['name'] +"</a>";
        }
    };
    listGroup += "</div>";
    $('#detail_display').append(listGroup);
    $('#detail_display div a').on('click', function(e){

        id = $(this).attr('id');
        url = "/restapi/testcaseresult/?id=" + id;
        var testcaseResult = httpGet(url);
        testcaseResult.done(function(data){
            if (data['result'] == "PASS"){
                $('#test_case_result_detail_header').attr("class", "modal-title btn btn-primary");
            }else {
                $('#test_case_result_detail_header').attr("class", "modal-title btn btn-danger");
            }
            $('#test_case_result_detail_name').text(data['testcase']['name']);
            $('#test_case_result_detail_request_url').text(data['testcase']['request_URL']);
            $('#test_case_result_detail_request_headers').text(data['testcase']['request_headers']);
            $('#test_case_result_detail_request_body').text(data['testcase']['request_body']);
            $('#test_case_result_detail_real_status').text(data['real_status']);
            $('#test_case_result_detail_expected_status').text(data['testcase']['expected_response']);
            $('#test_case_result_detail_real_data').text(data['real_response']);
            $('#test_case_result_detail_expected_data').text(data['testcase']['expected_data']);
            $("#test_case_result_detail").modal();
        })
    });
};


$('#new').on('click', function(e){

    $('#new_test_run').modal();

})

$("#add_new_run").on('click', function(e){
    e.preventDefault();
    feature = $('#id_feature :selected').text();
    level = $('#id_level :selected').text();
    status = $('#id_status :selected').text();
    request_method = $('#id_request_method :selected').text();

    url = "/restapi/testrun/";
    content = {
        "status": status,
        "level": level,
        "feature": feature,
        "request_method": request_method
    };
    $('#new_test_run').modal('hide');
    document.getElementById("ldiv").style.display = "block";
    testrun = httpPost(url, content);
    testrun.done(function(data){
        $('#ldiv').hide();
        location.reload();
    });
    document.getElementById("ldiv").style.display = "display:none;";

})
