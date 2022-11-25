$(".activate-form").submit(function(e){
    e.preventDefault();
    var action_url = $(this).attr("action")
    formData = new FormData($(this).get(0));
    $.ajax({
        type: "POST",
        url: action_url,
        data: formData,
        contentType: false,
        processData: false,
        success: function(response){
            if ("success" in response){
                body = document.querySelector(".active")
                body.classList.remove("closing")
            }
        }
    })
})