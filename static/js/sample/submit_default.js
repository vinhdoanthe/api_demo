$(document).on('submit', '#default-form',function(e){
    e.preventDefault()
    let data = {
            number_of_items:$('input[name=number_of_items]').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        };


    $.ajax({
        type: 'POST',
        url: "/api/long-running-task/",
        data: data,
        success:function(json){
            document.getElementById("default-form").reset();
            $("#result").prepend('<p>'+
                'Task success'+
            '</p>'
            )
        },
        error : function(xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});