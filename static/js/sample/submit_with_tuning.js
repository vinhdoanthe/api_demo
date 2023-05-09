let isActive = true;
let isCheckTaskProgressActive = false;

$(document).on('submit', '#tuning-form', function (e) {
    e.preventDefault()
    let data = {
        number_of_items: $('input[name=number_of_items]').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    };


    $.ajax({
        type: 'POST',
        url: "/api/tuned-long-running-task/",
        data: data,
        success: function (json) {
            $("#result").html('<p>' +
                '<p>Task id: ' + json.data.task_id + '</p>' +
                '</p>'
            )
            if (isCheckTaskProgressActive === false) {
                isActive = true;
                isCheckTaskProgressActive = true;
                pollCheckTaskProgress(json.data.task_id)
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});

function pollCheckTaskProgress(task_id) {
    if (isActive) {
        window.setTimeout(function () {
            $.ajax({
                url: "api/tuned-long-running-task/" + task_id + "/",
                type: "GET",
                success: function (result) {
                    if (result.data.task_status !== "SUCCESS") {
                        $("#result").prepend(
                            '<p>% done: ' + result.data.done_percentage + '</p>'
                        )
                        pollCheckTaskProgress(task_id)
                    } else {
                        $("#result").prepend(
                            '<p>Task success</p>'
                        )
                        isActive = false;
                        isCheckTaskProgressActive = false;
                    }
                },
                error: function () {
                    pollCheckTaskProgress(task_id);
                }
            });
        }, 1000);
    }
}