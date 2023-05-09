$(document).on('submit', '#default-form', function (e) {
    e.preventDefault()

    $("#result").html(
                "<span>Lets wait for the task to complete. This may take a while...</span>"
    );

    let data = {
        number_of_items: $('input[name=number_of_items]').val(),
    };

    $.ajax({
        type: 'POST',
        url: "/api/long-running-task/",
        data: data,
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (json) {
            $("#result").html(
                '<p>' +
                'Task success' +
                '</p>'
            )
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});