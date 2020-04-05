
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

let table = $('#datatables').DataTable({
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": "/restapi/testcase/",
        "type": "GET",
//        "dataSrc": ""
    },

    "columnDefs": [
            {
                "targets": [ 0 ],
                "visible": false,
                "searchable": false
            },
    ],

    "columns": [
            {"data": "id"},
            {"data": "name"},
            {"data": "feature.name"},
            {"data": "level.name"},
            {"data": "request_method.name"},
            {"data": "created_by.username"},
            {
                "data": null,
                "defaultContent": '<button type="button" class="btn btn-primary">Detail</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-info">Edit</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-danger">Delete</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-warning">Test</button>'
            }

    ],
});

let id = 0;

$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info') {
        // EDIT button
        $('#id_name').val(data['name']);
        $('#id_feature').val(data['feature']['id']);
        $('#id_level').val(data['level']['id']);
        $('#id_status').val(data['status']['id']);
        $('#id_request_method').val(data['request_method']['id']);
        $('#id_request_headers').val(data['request_headers']);
        $('#id_request_URL').val(data['request_URL']);
        $('#id_request_body').val(data['id_request_body']);
        $('#id_expected_data').val(data['expected_data']);
        $('#id_expected_response').val(data['expected_response']);
        $('#form_type').val('edit');
        $('#modal_title').text('EDIT');
        $("#myModal").modal();
    } else if (class_name == 'btn btn-primary'){
        // Detail button
        $("#test_case_name").text(data['name']);
        $("#test_case_status").text(data['status']['name']);
        $("#test_case_level").text(data['level']['name']);
        $("#test_case_created_by").text(data['created_by']['username']);
        $("#test_case_feature").text(data['feature']['name']);
        $("#test_case_request_method").text(data['request_method']['name']);
        $("#test_case_created_date").text(data['created_date']);
        $("#test_case_last_modify_date").text(data['last_modify_date']);
        $("#test_case_request_url").text(data['request_URL']);
        $("#test_case_request_headers").text(data['request_headers']);
        $("#test_case_request_body").text(data['request_body']);
        $("#test_case_expected_response").text(data['expected_response']);
        $("#test_case_expected_data").text(data['expected_data']);
        $("#detail").modal();
    } else if (class_name == 'btn btn-warning'){
        let $this = $(this);
        document.getElementById("ldiv").style.display = "block";

        $.ajax({
                    url: '/restapi/testrun/',
                    method: "POST",
                    data: {"testcases":data['id']},
                    headers:{
                        "X-CSRFTOken": getCookie('csrftoken')
                            }
                }).done(function (data, textStatus, jqXHR) {
                    $('#ldiv').hide();
                    if (data["details"][0]["result"] == "PASS"){
                        $('#result_header').attr("class", "modal-title btn btn-primary");
                        $('#result_title').text('PASS');
                    } else {
                        $('#result_header').attr("class", "modal-title btn btn-danger");
                        $('#result_title').text('FAILED');
                    }
                    $('#test_result_expected_status').text(data["details"][0]["testcase"]["expected_response"]);
                    $('#test_result_real_status').text(data["details"][0]["real_status"]);
                    $('#test_result_expected_data').text(data["details"][0]["testcase"]["expected_data"]);
                    $('#test_result_real_data').text(data["details"][0]["real_response"]);
                    $("#result").modal();

                })
        document.getElementById("ldiv").style.display = "display:none;";

    } else {
        // DELETE button
        $('#modal_title').text('DELETE');
        $("#confirm").modal();
    }
    id = data['id'];
});

$('#test_case_form').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let type = $('#form_type').val();
    let method = '';
    let url = '/restapi/testcase/';
    if (type == 'new') {
        // new
        method = 'POST';
    }else if(type == 'edit'){
        // edit
        url = url + "?id=" + id + '';
        method = 'PUT';
    } else{
        
        return;
    };
    $.ajax({
        url: url,
        method: method,
        headers: {
            "X-CSRFTOken": getCookie('csrftoken')
                },
        data: $this.serialize(),
    }).done(function (data, textStatus, jqXHR) {
        location.reload();

    })
});



$('#confirm').on('click', '#delete', function (e) {

    var token = getCookie('csrftoken');
    $.ajax({
        url: '/restapi/testcase/?id=' + id + '',
        method: 'DELETE',
        headers:{
            "X-CSRFTOken": getCookie('csrftoken')
        }
    }).done(function (data, textStatus, jqXHR) {
        location.reload();
    })
});

$('#new').on('click', function (e) {
    $('#form_type').val('new');
    $('#modal_title').text('New Test Case');
    $("#myModal").modal();

});

$('#save').on('click', function(e){

    location.reload();

});

function submit_form(){

    let $this = $(this);
    let type = $('#form_type').val();
    let method = '';
    let url = '/restapi/testcase/';
    if (type == 'new') {
        // new
        method = 'POST';
    }else if(type == 'edit'){
        // edit
        url = url + "?id=" + id + '';
        method = 'PUT';
    } else{
        
        return;
    };
    $.ajax({
        url: url,
        method: method,
        headers: {
            "X-CSRFTOken": getCookie('csrftoken')
                },
        data: $this.serialize(),
    }).done(function (data, textStatus, jqXHR) {
        location.reload();

    })
}
