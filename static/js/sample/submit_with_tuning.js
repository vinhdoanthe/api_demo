$(document).on('submit', '#tuning-form',function(e){
    e.preventDefault()
    let data = {
            number_of_items:$('input[name=number_of_items]').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        };


    $.ajax({
        type: 'POST',
        url: "/api/tuned-long-running-task/",
        data: data,
        success:function(json){
            document.getElementById("tuning-form").reset();
            console.log(json)
            $("#result").prepend('<p>'+
                '<p>Task id: ' + json.data.task_id + '</p>'+
            '</p>'
            )
        },
        error : function(xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});