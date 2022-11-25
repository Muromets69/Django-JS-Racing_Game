const point = document.querySelector('.point') 
var seconds = 4
point.innerHTML = `Упс... ошибочка переадресация на главную страницу. Через - ${seconds}`  
setTimeout(function () {
    point.innerHTML = `Упс... ошибочка переадресация на главную страницу. Через - ${seconds}`
    if (seconds==0){
        window.location.replace(point.href)
    }
    seconds--;
}, 1000);