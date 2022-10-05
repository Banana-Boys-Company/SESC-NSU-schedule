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

let time_lst = ["1(8:30)", "2(9:15)", "3(10:20)", "4(11:25)", "5(12:30)", "6(13:25)"]

let weekDay_title = [
'    <div class="tab-pane fade show active" id="pills-Monday" role="tabpanel" aria-labelledby="pills-Monday-tab">',
'    <div class="tab-pane fade" id="pills-Tuesday" role="tabpanel" aria-labelledby="pill-Tuesday-tab">',
'    <div class="tab-pane fade" id="pills-Wednesday" role="tabpanel" aria-labelledby="pill-Wednesday-tab">',
'    <div class="tab-pane fade" id="pills-Thursday" role="tabpanel" aria-labelledby="pill-Thursday-tab">',
'    <div class="tab-pane fade" id="pills-Friday" role="tabpanel" aria-labelledby="pill-Friday-tab">',
'    <div class="tab-pane fade" id="pills-Saturday" role="tabpanel" aria-labelledby="pill-Saturday-tab">'
]

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


    let toggle_1 = 0;
    let toggle_2 = 0;
    let toggle_3 = 0;
    $(".child-toggle-1").on("click", function () {
        if (toggle_1>= 1) {
            $(".child-window-menu-1").toggle();
            $(".child-window-menu-2").hide();
            $(".child-window-menu-3").hide();
        }
        toggle_1++;
    });

    // Нажатие на дочерние меню 10 класса
    $(".child-toggle-2").on("click", function () {
        if (toggle_2 >= 1) {
            $(".child-window-menu-2").toggle();
            $(".child-window-menu-1").hide();
            $(".child-window-menu-3").hide();
        }
        toggle_2++;
    });

    // Нажатие на дочерние меню 11 класса
    $(".child-toggle-3").on("click", function () {
        if (toggle_3 >= 1) {
            $(".child-window-menu-3").toggle();
            $(".child-window-menu-1").hide();
            $(".child-window-menu-2").hide();
        }
        toggle_3++;
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
        generate_schedule_table(data, weekDay_title, time_lst)
    }
})

// Генерация расписания на основе данных с сервера
function generate_schedule_table(data, weekDay_title, time_lst) {
    $('#main-page').empty() // отчистка места появления таблицы
    let start = `<ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation">
    <button class="nav-link active" id="pills-Monday-tab" data-bs-toggle="pill" data-bs-target="#pills-Monday"
    type="button" role="tab" aria-controls="Monday" aria-selected="true">Пн</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="nav-link" id="pills-Tuesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Tuesday" type="button"
    role="tab" aria-controls="week-Tuesday" aria-selected="false">Вт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="nav-link" id="pills-Wednesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Wednesday"
    type="button" role="tab" aria-controls="week-Wednesday" aria-selected="false">Ср</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="nav-link" id="pills-Thursday-tab" data-bs-toggle="pill" data-bs-target="#pills-Thursday"
    type="button" role="tab" aria-controls="week-Thursday" aria-selected="false">Чт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="nav-link" id="pills-Friday-tab" data-bs-toggle="pill" data-bs-target="#pills-Friday" type="button"
    role="tab" aria-controls="week-Friday" aria-selected="false">Пт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="nav-link" id="pills-Saturday-tab" data-bs-toggle="pill" data-bs-target="#pills-Saturday"
    type="button" role="tab" aria-controls="week-Saturday" aria-selected="false">Сб</button>
    </li>
    </ul>
    <div class="tab-content" id="weeks-tabContent">`// 6 базовых кнопок в начале
    for (let i = 0; i <= 5; i++) {
        start += weekDay_title[i] // добавление начала нужной вкладки из констант
        start += '<table class="table table-bordered"><thead><tr><th scope="col" id="time">№ Урока</th><th scope="col">Урок</th></tr></thead><tbody>' //Первая строчка таблицы №Урока и Урок
        timer = 0 // таймер для уроков(максимум 6)
        for (let element in data[Object.keys(data)[i]]) {// циклом проходимся по каждому двумерному списку словаря используя ключи строго от monday к saturday            
            let shablon = "" // в этом цикле создаем переменную шаблон для генерирования в ней самой таблицы каждого дня
            shablon += `<tr><th scope="row" id="time">${time_lst[timer]}</th>`//прибавляем время
            timer += 1
            if (data[Object.keys(data)[i]][element][1] > 1) { // если высота строки больше 1
                shablon += `<td rowspan="${data[Object.keys(data)[i]][element][1]}" style="vertical-align: middle;">${data[Object.keys(data)[i]][element][0]}</td></tr>` // задаем эту строку нужной высоты и добавляем стиль вертикального центрирования
                while (data[Object.keys(data)[i]][element][1] > 1){ // надо добавить h-1 пустых строк, чтобы таблица не сломалась(h - высота строки)
                    shablon += `<tr><th scope="row" id="time">${time_lst[timer]}</th></tr>`
                    timer += 1 // В первом столбце всегда будет 6 рядов, поэтому каждый раз генерим новую строку для 1 столбца и увеличиваем таймер
                    data[Object.keys(data)[i]][element][1] -= 1} // уменьшаем высоту уже выбранной строки, чтобы цикл не зациклился
                }
                else { // длинна строки может быть только 1, значит добавляем к шаблону f-строку с заданной высотой
                    shablon += `<td rowspan="1">${data[Object.keys(data)[i]][element][0]}</td></tr>`
                }
                start += shablon // в конце прибавляем к start сморфированную таблицу
            }
            start += "</tbody></table></div>" // закрываем все теги
        }
        start += "</div>" // закрываем последний тег
        $('#main-page').append(start) //добавляем таблицу на страничку

    }
