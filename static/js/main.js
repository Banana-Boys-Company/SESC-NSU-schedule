// [^-^]Hikaru#7106 - лучший кодер в мире

// Подсоединение к сокет серверу бэка
const socket = io.connect("http://127.0.0.1:80")

// Таймер неактивности, поистечению 5 минут перезагрузка
var timer = setTimeout(function () {
    location.reload();
}, 300000)

// Тестовый запрос к серверу
socket.on('connect', () => {
    socket.send({ 'status': 200 })
})

// Код после полной загрузки страницы
$(document).ready(function () {
    // Выбор группы класса
    $('.get-table').on("click", function (el) {
        $(".child-window-menu-1").hide();
        $(".child-window-menu-2").hide(); 
        $(".child-window-menu-3").hide(); 

        console.log("Send data")
        socket.emit('getClassData', { 'item_id': el.target.id });
    });


    // Изменение цвета ссылок


    // Нажатие на дочерние меню 9 класса
    $(".child-toggle-1").on("click", function () {
        $(".child-window-menu-1").toggle();
        $(".child-window-menu-2").hide();
        $(".child-window-menu-3").hide();
  });

    // Нажатие на дочерние меню 10 класса
     $(".child-toggle-2").on("click", function () {
        $(".child-window-menu-2").toggle();
        $(".child-window-menu-1").hide();
        $(".child-window-menu-3").hide();
  });

    // Нажатие на дочерние меню 11 класса
      $(".child-toggle-3").on("click", function () {
        $(".child-window-menu-3").toggle();
        $(".child-window-menu-1").hide();
        $(".child-window-menu-2").hide();
  });


    // Перезапуск таймера при активности
    $('html').click(function () {
        clearTimeout(timer);
        timer = setTimeout(function () {
            location.reload();
        }, 300000)
    });
});

// Получение данных расписания с сервера
socket.on('schedule', data => {
    console.log(data)
    if (data["status"] === 200) {
        console.log("Connection success!")
    }
    //generate_schedule_table(data)
})

// Генерация расписания на основе данных с сервера
// function generate_schedule_table(data) {
//     console.log("Generating shedule table...")
//     ...
// }

