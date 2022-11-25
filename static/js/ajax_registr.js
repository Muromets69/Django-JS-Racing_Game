$(".form-reg").submit(function(e){
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
                document.querySelector('.form-erros-signup').innerHTML = "<b>Created!</b>"
            }
            else if("error" in response){
                document.querySelector('.form-erros-signup').innerHTML = "<b>Возможние ошибки создания:</b>"
                for (let key in response["error"]) {
                    document.querySelector('.form-erros-signup').innerHTML += "</br>" + response["error"][key]
                }
            }
        }
    })
})
$(".form-log").submit(function(e){
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
                location.reload()
            }
            else if("error" in response){
                document.querySelector('.form-erros-login').innerHTML = response["error"]
            }
        }
    })
})
