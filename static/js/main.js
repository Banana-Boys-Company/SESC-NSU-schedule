// [^-^]Hikaru#7106 - лучший кодер в мире

// Подсоединение к сокет серверу бэка
const socket = io.connect("http://127.0.0.1:80")

// Таймер неактивности, поистечению 5 минут перезагрузка
var timer_ = setTimeout(function () {
    location.reload();
}, 10000)

socket.on('response-banner', data => {
    let banner_links = []
    Array.from($('.banner-element')).forEach(function (el) {
        banner_links.push(el.children[0].getAttribute('src').replace("/static/", ""));
    });
    let is_same = (data['new_data'].length == banner_links.length) && data['new_data'].every(function (element, index) {

        return element === banner_links[index];
    });
    if (data['old_data'] != []) {
        let old_banners = []
        Array.from($('.banner-element')).forEach(function (el) {
            let this_src = el.children[0].getAttribute('src').replace("/static/", "");
            if (data['old_data'].includes(this_src)) {
                el.parentNode.removeChild(el);
            }
        });
    }
    let difference = data['new_data'].filter(x => !banner_links.includes(x));
    difference.forEach(function (item, i, difference) {
        $("#carousel").append(`<div class="carousel-item banner-element"><img src="/static/${item}" class="d-block w-100" alt="Баннер"></div>`)
    });
})

// Тестовый запрос к серверу
socket.on('connect', () => {
    socket.send({ 'status': 200 })
})

let time_lst = ["1(8:30)", "2(9:15)", "3(10:20)", "4(11:25)", "5(12:30)", "6(13:25)", "6,5(15:00)", "7(16:00)", "8(16:50)", "9(18:00)", "10(18:50)", "11(20:30)", "12(21:20)"]

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

    $(".get-course").on("click", function (el) {
        $('#banner').css({ 'visibility': 'hidden', 'display': 'none' })
        if (window.innerWidth > 992) {
            $(".classbutton").removeClass("show")
            $(".dropdown-menu").removeClass("show")
        }
        socket.emit('getСoursesData', { 'item_id': el.target.id });
    })

    $('.get-table').on("click", function (el) {

        $('#banner').css({ 'visibility': 'hidden', 'display': 'none' })

        if (window.innerWidth > 992) {
            $(".classbutton").removeClass("show")
            $(".dropdown-menu").removeClass("show")
        }

        socket.emit('getClassData', { 'item_id': el.target.id });
    });



    $('html').click(function () {
        clearTimeout(timer_);
        timer_ = setTimeout(function () {
            location.reload();
        }, 100000)
    });

    


    $(".dropdown-menu").each(function(element) {

        this.click(function (el) {
            el.stopPropagation();
        })});
    document.querySelectorAll('.dropdown-menu').forEach(function(element){
        element.addEventListener('click', function (e) {
          e.stopPropagation();
      });
    })



        // make it as accordion for smaller screens
        if (window.innerWidth < 992) {

  // close all inner dropdowns when parent is closed
  document.querySelectorAll('.navbar .dropdown').forEach(function(everydropdown){
    everydropdown.addEventListener('hidden.bs.dropdown', function () {
      // after dropdown is hidden, then find all submenus
      this.querySelectorAll('.submenu').forEach(function(everysubmenu){
          // hide every submenu as well
          everysubmenu.style.display = 'none';

      });
  })
});
  document.querySelectorAll('.dropdown-menu a').forEach(function(element){
    element.addEventListener('click', function (e) {
        let fuck = document.getElementById("navbarSupportedContent")
        let nextEl = this.nextElementSibling;
        if(nextEl && nextEl.classList.contains('submenu')) {    
          // prevent opening link if link needs to open dropdown
          e.preventDefault();
          if(nextEl.style.display == 'block'){
            nextEl.style.display = 'none';
        } else {
            nextEl.style.display = 'block';
        }
    }
    else {
        fuck.classList.remove("show")
    }
});
})
}
})



// Получение данных расписания с сервера
socket.on('schedule', data => {
    if (data["status"] === 200) {
        console.log("Connection success!")
        generate_schedule_table(data, weekDay_title, time_lst)
    }
})

socket.on('courses', data => {
    console.log("Connection success!")
    console.log(data)
    generate_courses_table(data)
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
                while (data[Object.keys(data)[i]][element][1] > 1) { // надо добавить h-1 пустых строк, чтобы таблица не сломалась(h - высота строки)
                    shablon += `<tr><th scope="row" id="time">${time_lst[timer]}</th></tr>`
                    timer += 1 // В первом столбце всегда будет 6 рядов, поэтому каждый раз генерим новую строку для 1 столбца и увеличиваем таймер
                    data[Object.keys(data)[i]][element][1] -= 1
                } // уменьшаем высоту уже выбранной строки, чтобы цикл не зациклился
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

};

function generate_courses_table(data) {
    let const_ = '<table class="table table-bordered"><thead><tr><th scope="col" id="time">№ Урока</th><th scope="col">Урок</th></tr></thead><tbody>';
    let specDayTab = [
        '<div class="tab-pane fade show active" id="pills-Monday" role="tabpanel" aria-labelledby="pills-Monday-tab">',
        '<div class="tab-pane fade" id="pills-Tuesday" role="tabpanel" aria-labelledby="pill-Tuesday-tab">',
        '<div class="tab-pane fade" id="pills-Wednesday" role="tabpanel" aria-labelledby="pill-Wednesday-tab">',
        '<div class="tab-pane fade" id="pills-Thursday" role="tabpanel" aria-labelledby="pill-Thursday-tab">',
        '<div class="tab-pane fade" id="pills-Friday" role="tabpanel" aria-labelledby="pill-Friday-tab">',
        '<div class="tab-pane fade" id="pills-Saturday" role="tabpanel" aria-labelledby="pill-Saturday-tab">',
        '<div class="tab-pane fade" id="pills-Sunday" role="tabpanel" aria-labelledby="pill-Sunday-tab">',
    ];
    let weekDay_title = [
        '<div class="tab-pane fade show active" id="pills-Monday" role="tabpanel" aria-labelledby="pills-Monday-tab">',
        '<div class="tab-pane fade" id="pills-Tuesday" role="tabpanel" aria-labelledby="pill-Tuesday-tab">',
        '<div class="tab-pane fade" id="pills-Wednesday" role="tabpanel" aria-labelledby="pill-Wednesday-tab">',
        '<div class="tab-pane fade" id="pills-Thursday" role="tabpanel" aria-labelledby="pill-Thursday-tab">',
        '<div class="tab-pane fade" id="pills-Friday" role="tabpanel" aria-labelledby="pill-Friday-tab">',
        '<div class="tab-pane fade" id="pills-Saturday" role="tabpanel" aria-labelledby="pill-Saturday-tab">',
        '<div class="tab-pane fade" id="pills-Sunday" role="tabpanel" aria-labelledby="pill-Sunday-tab">'
    ];
    $('#main-page').empty()
    code = '<ul class="nav nav-pills mb-3" id="pills-tab" role="tablist"><li class="nav-item" role="presentation"><button class="nav-link active" id="pills-Monday-tab" data-bs-toggle="pill" data-bs-target="#pills-Monday"type="button" role="tab" aria-controls="Monday" aria-selected="true">Пн</button></li><li class="nav-item" role="presentation"><button class="nav-link" id="pills-Tuesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Tuesday" type="button"role="tab" aria-controls="week-Tuesday" aria-selected="false">Вт</button></li><li class="nav-item" role="presentation"><button class="nav-link" id="pills-Wednesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Wednesday"type="button" role="tab" aria-controls="week-Wednesday" aria-selected="false">Ср</button></li><li class="nav-item" role="presentation"><button class="nav-link" id="pills-Thursday-tab" data-bs-toggle="pill" data-bs-target="#pills-Thursday"type="button" role="tab" aria-controls="week-Thursday" aria-selected="false">Чт</button></li><li class="nav-item" role="presentation"><button class="nav-link" id="pills-Friday-tab" data-bs-toggle="pill" data-bs-target="#pills-Friday" type="button"role="tab" aria-controls="week-Friday" aria-selected="false">Пт</button></li><li class="nav-item" role="presentation"><button class="nav-link" id="pills-Saturday-tab" data-bs-toggle="pill" data-bs-target="#pills-Saturday"type="button" role="tab" aria-controls="week-Saturday" aria-selected="false">Сб</button></li><li class="nav-item" role="presentation"><button class="nav-link" id="pills-Sunday-tab" data-bs-toggle="pill" data-bs-target="#pills-Sunday"type="button" role="tab" aria-controls="week-Saturday" aria-selected="false">Вс</button></li></ul><div class="tab-content" id="weeks-tabContent">'
    console.log("start")
    for (let z = 0; z <= 6; z++) {
        code += weekDay_title[z];
        code += '<table class="table table-bordered"><thead><tr><th scope="col" id="time">Время</th><th scope="col">Спец-курс</th></tr></thead><tbody>';
        lowerLevel = data[Object.keys(data)[z]]
        for (i in lowerLevel) {
            if (lowerLevel[i].length != 0) {
                code += `<tr><th rowspan="${lowerLevel[i].length}">${i}</th><td>${lowerLevel[i][0]}</td></tr>`;
                for (let j = 0; j <= lowerLevel[i].length - 1; j++) {
                    code += `<tr><td>${lowerLevel[i][j]}</td></tr>`;
                }
            }
        }
        code += "</tbody></table></div>";
    }
    code += "</div>"
    $('#main-page').append(code)
}


function timeCount() {
    var today = new Date();

    var day = today.getDate();
    var month = today.getMonth()+1;
    var year = today.getFullYear();

    var hour = today.getHours();
    if(hour<10)hour = "0"+hour;

    var minute = today.getMinutes();
    if(minute<10)minute = "0"+minute;

    var second = today.getSeconds();
    if(second<10)second = "0"+second;

    document.getElementById("clock").innerHTML = 
    day+"/"+month+"/"+year+" | "+hour+":"+minute+":"+second;

    setTimeout("timeCount()", 1000);
}