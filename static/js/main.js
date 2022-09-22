const socket = io.connect("http://127.0.0.1:80")
var timer = setTimeout(function () {
    location.reload();
}, 300000)

socket.on('connect', () => {
    socket.send({ 'status': 200 })
})

$(document).ready(function () {
    $('.get-table').on("click", function (el) {
        console.log("Send data")
        socket.emit('getClassData', { 'item_id': el.target.id });
    });
    $('html').click(function () {

        console.log("clicked")
        clearTimeout(timer);
        timer = setTimeout(function () {
            location.reload();
        }, 300000)
    });
});

socket.on('schedule', data => {
    console.log(data)
    if (data["status"] === 200) {
        console.log("Connection success!")
    }
})