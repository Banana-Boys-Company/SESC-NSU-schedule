// [^-^]Hikaru#7106 - лучший кодер в мире

// Подсоединение к сокет серверу бэка
const socket = io.connect("http://127.0.0.1:80")

// Таймер неактивности, поистечению 5 минут перезагрузка
var timer_ = setTimeout(function () {
    if ($('#banner').css('display') == 'none') {
        location.reload();
    }
}, 100000)

let element_id = ""
let click = true

var today = new Date();
let weekday = today.getDate()

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

let time_lst = ["1(8:30)", "2(9:15)", "3(10:20)", "4(11:25)", "5(12:30)", "6(13:25)", "(15:00)", "7(16:00)", "8(16:50)", "9(18:00)", "10(18:50)", "11(20:30)", "12(21:20)"]


// Код после полной загрузки страницы
$(document).ready(function () {
    $(document).on("click", ".close-warning", function (el) {
        let alert_message = $(this).parent(".alert");
        alert_message.remove()
    });

    $(document).on("click", '.weekday-button', function (el) {
        if (click == true) {
            click = false;
            buttonTimeOut();
        } else {
            let new_warning =
                $(`<div class="alert alert-warning w-75 float-end align-items-center" id="timeout-alert">
                    <svg class="bi flex-shrink-0 me-2" width="24" height="24">
                        <use xlink:href="#warning" />
                    </svg>
                    <button type="button" class="close-warning float-end btn align-center" data-dismiss="alert">x</button>
                    <strong class="">Предупреждение!</strong>
                    <p class="text-start text-wrap">Подождите немного перед повторным использованием</p>
                    <div class="progress">
                        <div class="progress-bar" role="progressbar progress-bar-striped progress-bar-animated"
                            aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
                        </div>
                    </div>
                </div>`)
            $("#error-modal").append(new_warning)
            $("#error-modal").children().slice(-1)[0]
            $(".weekday-button").attr({ "aria-disabled": "true" }).addClass('disabled')
            new_warning.fadeTo(2000, 500).slideUp(500, function () {
                new_warning.slideUp(500);
                new_warning.children(".progress")
            });
            let progressBar = $($($($("#error-modal").children().slice(-1)[0]).children(".progress")).children(".progress-bar"))
            progressBar.animate({ width: "0%" }, 1500);
            progressBar.delay(1000).fadeOut(250);
        }

    });
    function buttonTimeOut() {
        setTimeout(function () {
            click = true;
            $(".weekday-button").attr({ "aria-disabled": "false" }).removeClass('disabled')
            console.log('Теперь можете нажимать')
        }, 500)
    };
    // Выбор группы класса

    $(".get-class").on("click", function (el) {
        $('#banner').css({ 'visibility': 'hidden', 'display': 'none' })
        if (window.innerWidth > 992) {
            $(".classbutton").removeClass("show")
            $(".dropdown-menu").removeClass("show")
        }
        element_id = el.target.id
        socket.emit('getClassData', { 'item_id': el.target.id, 'get_all': true });
    });

    $(".get-course").on("click", function (el) {
        $('#banner').css({ 'visibility': 'hidden', 'display': 'none' })
        if (window.innerWidth > 992) {
            $(".classbutton").removeClass("show")
            $(".dropdown-menu").removeClass("show")
        }
        socket.emit('getСoursesData', { 'item_id': el.target.id });
    });

    $('.get-table').on("click", function (el) {

        $('#banner').css({ 'visibility': 'hidden', 'display': 'none' })

        if (window.innerWidth > 992) {
            $(".classbutton").removeClass("show")
            $(".dropdown-menu").removeClass("show")
        }
        element_id = el.target.id
        socket.emit('getClassData', { 'item_id': el.target.id });
    });



    $('html').click(function () {
        clearTimeout(timer_);
        timer_ = setTimeout(function () {
            if ($('#banner').css('display') == 'none') {
                location.reload();
            }
        }, 100000)
    });




    $(".dropdown-menu").each(function (element) {

        this.click(function (el) {
            el.stopPropagation();
        })
    });
    document.querySelectorAll('.dropdown-menu').forEach(function (element) {
        element.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    });



    // make it as accordion for smaller screens
    if (window.innerWidth < 992) {

        // close all inner dropdowns when parent is closed
        document.querySelectorAll('.navbar .dropdown').forEach(function (everydropdown) {
            everydropdown.addEventListener('hidden.bs.dropdown', function () {
                // after dropdown is hidden, then find all submenus
                this.querySelectorAll('.submenu').forEach(function (everysubmenu) {
                    // hide every submenu as well
                    everysubmenu.style.display = 'none';

                });
            })
        });
        document.querySelectorAll('.dropdown-menu a').forEach(function (element) {
            element.addEventListener('click', function (e) {
                let fuck = document.getElementById("navbarSupportedContent")
                let nextEl = this.nextElementSibling;
                if (nextEl && nextEl.classList.contains('submenu')) {
                    // prevent opening link if link needs to open dropdown
                    e.preventDefault();
                    if (nextEl.style.display == 'block') {
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
});



// Получение данных расписания с сервера
socket.on('schedule', data => {
    if (data["status"] === 200) {
        if (data["get_all"] === true) {
            all_table(Object.values(data["data"]))
        } else {
            generate_schedule_table(data)
        }
    }
});

socket.on('courses', data => {
    generate_courses_table(data)
});

let week_pills = [null, "pills-Monday-tab", "pills-Tuesday-tab", "pills-Wednesday-tab", "pills-Thursday-tab", "pills-Friday-tab", "pills-Saturday-tab"]

// Генерация расписания на основе данных с сервера
function generate_schedule_table(data) {
    $('#main-page').empty() // отчистка места появления таблицы
    let response_data = element_id.split(":")
    let weekday = today.getDay()
    let weekDay_title = [
        `<div class="tab-pane fade${weekday == 1 ? "show active" : ""}" id="pills-Monday" role="tabpanel" aria-labelledby="pills-Monday-tab">`,
        `<div class="tab-pane fade${weekday == 2 ? "show active" : ""}" id="pills-Tuesday" role="tabpanel" aria-labelledby="pill-Tuesday-tab">`,
        `<div class="tab-pane fade${weekday == 3 ? "show active" : ""}" id="pills-Wednesday" role="tabpanel" aria-labelledby="pill-Wednesday-tab">`,
        `<div class="tab-pane fade${weekday == 4 ? "show active" : ""}" id="pills-Thursday" role="tabpanel" aria-labelledby="pill-Thursday-tab">`,
        `<div class="tab-pane fade${weekday == 5 ? "show active" : ""}" id="pills-Friday" role="tabpanel" aria-labelledby="pill-Friday-tab">`,
        `<div class="tab-pane fade${weekday == 6 ? "show active" : ""}" id="pills-Saturday" role="tabpanel" aria-labelledby="pill-Saturday-tab">`
    ]
    let start = `
    <p class="ml-3">${response_data[0].split("_")[0]}-${response_data[0].split("_")[1]} класс | ${response_data[1]} группа</p>
    <hr>
    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 1 ? " active" : ""}" id="pills-Monday-tab" data-bs-toggle="pill" data-bs-target="#pills-Monday"
    type="button" role="tab" aria-controls="Monday" aria-selected="${weekday == 1 ? "true" : "false"}">Пн</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 2 ? " active" : ""}" id="pills-Tuesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Tuesday" type="button"
    role="tab" aria-controls="week-Tuesday" aria-selected="${weekday == 2 ? "true" : "false"}">Вт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 3 ? " active" : ""}" id="pills-Wednesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Wednesday"
    type="button" role="tab" aria-controls="week-Wednesday" aria-selected="${weekday == 3 ? "true" : "false"}">Ср</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 4 ? " active" : ""}" id="pills-Thursday-tab" data-bs-toggle="pill" data-bs-target="#pills-Thursday"
    type="button" role="tab" aria-controls="week-Thursday" aria-selected="${weekday == 4 ? "true" : "false"}">Чт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 5 ? " active" : ""}" id="pills-Friday-tab" data-bs-toggle="pill" data-bs-target="#pills-Friday" type="button"
    role="tab" aria-controls="week-Friday" aria-selected="${weekday == 5 ? "true" : "false"}">Пт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 6 ? " active" : ""}" id="pills-Saturday-tab" data-bs-toggle="pill" data-bs-target="#pills-Saturday"
    type="button" role="tab" aria-controls="week-Saturday" aria-selected="${weekday == 6 ? "true" : "false"}">Сб</button>
    </li>
    </ul>
    <div class="tab-content" id="weeks-tabContent">`// 6 базовых кнопок в начале
    for (let i = 0; i <= 5; i++) {
        start += weekDay_title[i] // добавление начала нужной вкладки из констант
        start += '<table class="table table-bordered" style="width: 96%; margin-left: 2%; margin-right: 2%;"><thead><tr><th id="time">№ Урока</th><th style="text-align: center;">Урок</th></tr></thead><tbody>' //Первая строчка таблицы №Урока и Урок
        timer = 0 // таймер для уроков(максимум 6)
        for (let element in data[Object.keys(data)[i]]) {// циклом проходимся по каждому двумерному списку словаря используя ключи строго от monday к saturday            
            let shablon = "" // в этом цикле создаем переменную шаблон для генерирования в ней самой таблицы каждого дня
            shablon += `<tr><th id="time">${time_lst[timer]}</th>`//прибавляем время
            timer += 1
            if (data[Object.keys(data)[i]][element][1] > 1) { // если высота строки больше 1
                shablon += `<td rowspan="${data[Object.keys(data)[i]][element][1]}" style="vertical-align: middle;">${data[Object.keys(data)[i]][element][0]}</td></tr>` // задаем эту строку нужной высоты и добавляем стиль вертикального центрирования
                while (data[Object.keys(data)[i]][element][1] > 1) { // надо добавить h-1 пустых строк, чтобы таблица не сломалась(h - высота строки)
                    shablon += `<tr><th id="time">${time_lst[timer]}</th></tr>`
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
    if (weekday != 0) {
        $(`#${week_pills[weekday]}`).tab('show')
    } else {
        $("#pills-Monday-tab").tab('show');
    }
};

function generate_courses_table(data) {
    $('#main-page').empty()
    let weekday = today.getDay()
    let weekDay_title = [
        `<div class="tab-pane fade${weekday == 1 ? "show active" : ""}" id="pills-Monday" role="tabpanel" aria-labelledby="pills-Monday-tab">`,
        `<div class="tab-pane fade${weekday == 2 ? "show active" : ""}" id="pills-Tuesday" role="tabpanel" aria-labelledby="pill-Tuesday-tab">`,
        `<div class="tab-pane fade${weekday == 3 ? "show active" : ""}" id="pills-Wednesday" role="tabpanel" aria-labelledby="pill-Wednesday-tab">`,
        `<div class="tab-pane fade${weekday == 4 ? "show active" : ""}" id="pills-Thursday" role="tabpanel" aria-labelledby="pill-Thursday-tab">`,
        `<div class="tab-pane fade${weekday == 5 ? "show active" : ""}" id="pills-Friday" role="tabpanel" aria-labelledby="pill-Friday-tab">`,
        `<div class="tab-pane fade${weekday == 6 ? "show active" : ""}" id="pills-Saturday" role="tabpanel" aria-labelledby="pill-Saturday-tab">`,
        `<div class="tab-pane fade${weekday == 0 ? "show active" : ""}" id="pills-Sunday" role="tabpanel" aria-labelledby="pill-Sunday-tab">`
    ];
    code = `<ul class="nav nav-pills mb-3" style="padding-top: 10px" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation"><button class="weekday-button nav-link${today.getDay() == 1 ? " active" : ""}" id="pills-Monday-tab" data-bs-toggle="pill" data-bs-target="#pills-Monday"type="button" role="tab" aria-controls="Monday" aria-selected="${weekday == 1 ? "true" : "false"}">Пн</button></li>
    <li class="nav-item" role="presentation"><button class="weekday-button nav-link${today.getDay() == 2 ? " active" : ""}" id="pills-Tuesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Tuesday" type="button"role="tab" aria-controls="week-Tuesday" aria-selected="${weekday == 2 ? "true" : "false"}">Вт</button></li>
    <li class="nav-item" role="presentation"><button class="weekday-button nav-link${today.getDay() == 3 ? " active" : ""}" id="pills-Wednesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Wednesday"type="button" role="tab" aria-controls="week-Wednesday" aria-selected="${weekday == 3 ? "true" : "false"}">Ср</button></li>
    <li class="nav-item" role="presentation"><button class="weekday-button nav-link${today.getDay() == 4 ? " active" : ""}" id="pills-Thursday-tab" data-bs-toggle="pill" data-bs-target="#pills-Thursday"type="button" role="tab" aria-controls="week-Thursday" aria-selected="false${weekday == 5 ? "true" : "false"}">Чт</button></li>
    <li class="nav-item" role="presentation"><button class="weekday-button nav-link${today.getDay() == 5 ? " active" : ""}" id="pills-Friday-tab" data-bs-toggle="pill" data-bs-target="#pills-Friday" type="button"role="tab" aria-controls="week-Friday" aria-selected="${weekday == 6 ? "true" : "false"}">Пт</button></li>
    <li class="nav-item" role="presentation"><button class="weekday-button nav-link${today.getDay() == 6 ? " active" : ""}" id="pills-Saturday-tab" data-bs-toggle="pill" data-bs-target="#pills-Saturday"type="button" role="tab" aria-controls="week-Saturday" aria-selected="${weekday == 0 ? "true" : "false"}">Сб</button></li>
    <li class="nav-item" role="presentation"><button class="weekday-button nav-link${today.getDay() == 0 ? " active" : ""}" id="pills-Sunday-tab" data-bs-toggle="pill" data-bs-target="#pills-Sunday" type="button" role="tab" aria-controls="week-Sunday" aria-selected="false${weekday == 0 ? "true" : "false"}">Вс</button></li></ul><div class="tab-content" id="weeks-tabContent">`
    for (let z = 0; z <= 6; z++) {
        code += weekDay_title[z];
        code += '<table class="table table-bordered" style="width: 96%; margin-left: 2%; margin-right: 2%;"><thead><tr><th  id="time">Время</th><th style="text-align: center;">Спец-курс</th></tr></thead><tbody>';
        lowerLevel = data[Object.keys(data)[z]]
        for (i in lowerLevel) {
            if (lowerLevel[i].length != 0) {
                code += `<tr><th rowspan="${lowerLevel[i].length + 1}">${i}</th><td>${lowerLevel[i][0]}</td></tr>`;
                for (let j = 0; j <= lowerLevel[i].length - 1; j++) {
                    code += `<tr><td>${lowerLevel[i][j]}</td></tr>`;
                }
            }
        }
        code += "</tbody></table></div>";
    }
    code += "</div>"
    $('#main-page').append(code)
};
function all_table(data_lst) {
    $('#main-page').empty()
    let response_data = element_id.split(":")
    let only_for_all = response_data[1].split("_")
    let weekday = today.getDay()
    // Макс, я вот так достаю дочерние группы классов, оно работает, так что если не нравится
    // перепиши, а я спать хочу.
    let groups_names_str = ''
    $(`#${response_data[1]} > li > a`).each(function (index, element) {

        groups_names_str += `${$(element).attr("id")} `
    });
    groups_names = groups_names_str.split(' ')
    groups_names.shift()
    groups_names.pop()
    let gl = groups_names

    let weekDay_title = [
        `<div class="tab-pane fade${weekday == 1 ? "show active" : ""}" id="pills-Monday" role="tabpanel" aria-labelledby="pills-Monday-tab">`,
        `<div class="tab-pane fade${weekday == 2 ? "show active" : ""}" id="pills-Tuesday" role="tabpanel" aria-labelledby="pill-Tuesday-tab">`,
        `<div class="tab-pane fade${weekday == 3 ? "show active" : ""}" id="pills-Wednesday" role="tabpanel" aria-labelledby="pill-Wednesday-tab">`,
        `<div class="tab-pane fade${weekday == 4 ? "show active" : ""}" id="pills-Thursday" role="tabpanel" aria-labelledby="pill-Thursday-tab">`,
        `<div class="tab-pane fade${weekday == 5 ? "show active" : ""}" id="pills-Friday" role="tabpanel" aria-labelledby="pill-Friday-tab">`,
        `<div class="tab-pane fade${weekday == 6 ? "show active" : ""}" id="pills-Saturday" role="tabpanel" aria-labelledby="pill-Saturday-tab">`
    ]
    let start = `
    <p class="ml-3">${only_for_all[0]}-${only_for_all[1]} класс</p>
    <hr>
    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 1 ? " active" : ""}" id="pills-Monday-tab" data-bs-toggle="pill" data-bs-target="#pills-Monday"
    type="button" role="tab" aria-controls="Monday" aria-selected="${weekday == 1 ? "true" : "false"}">Пн</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 2 ? " active" : ""}" id="pills-Tuesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Tuesday" type="button"
    role="tab" aria-controls="week-Tuesday" aria-selected="${weekday == 2 ? "true" : "false"}">Вт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 3 ? " active" : ""}" id="pills-Wednesday-tab" data-bs-toggle="pill" data-bs-target="#pills-Wednesday"
    type="button" role="tab" aria-controls="week-Wednesday" aria-selected="${weekday == 3 ? "true" : "false"}">Ср</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 4 ? " active" : ""}" id="pills-Thursday-tab" data-bs-toggle="pill" data-bs-target="#pills-Thursday"
    type="button" role="tab" aria-controls="week-Thursday" aria-selected="${weekday == 4 ? "true" : "false"}">Чт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 5 ? " active" : ""}" id="pills-Friday-tab" data-bs-toggle="pill" data-bs-target="#pills-Friday" type="button"
    role="tab" aria-controls="week-Friday" aria-selected="${weekday == 5 ? "true" : "false"}">Пт</button>
    </li>
    <li class="nav-item" role="presentation">
    <button class="weekday-button nav-link${weekday == 6 ? " active" : ""}" id="pills-Saturday-tab" data-bs-toggle="pill" data-bs-target="#pills-Saturday"
    type="button" role="tab" aria-controls="week-Saturday" aria-selected="${weekday == 6 ? "true" : "false"}">Сб</button>
    </li>
    </ul>
    <div class="tab-content" id="weeks-tabContent">`
    for (let i = 0; i <= 5; i++) {
        start += weekDay_title[i] // добавление начала нужной вкладки из констант
        start += '<div class="container"><div class="row">'
        for (let j = 0; j < data_lst.length; j++) {
            let this_group = gl[j].split(':')[1]

            start += `<div class="col"><p>${this_group} группа</p><table class="table table-bordered"><thead><tr><th  id="time">№ Урока</th><th style="text-align: center;">Урок</th></tr></thead><tbody>` //Первая строчка таблицы №Урока и Урок
            timer = 0 // таймер для уроков(максимум 6)
            let data = data_lst[j]
            for (let element in data[(Object.keys(data))[i]]) {// циклом проходимся по каждому двумерному списку словаря используя ключи строго от monday к saturday            
                let shablon = "" // в этом цикле создаем переменную шаблон для генерирования в ней самой таблицы каждого дня
                shablon += `<tr><th  id="time">${time_lst[timer]}</th>`//прибавляем время
                timer += 1
                if (data[(Object.keys(data))[i]][element][1] > 1) { // если высота строки больше 1
                    shablon += `<td rowspan="${data[(Object.keys(data))[i]][element][1]}" style="vertical-align: middle;">${data[(Object.keys(data))[i]][element][0]}</td></tr>` // задаем эту строку нужной высоты и добавляем стиль вертикального центрирования
                    while (data[(Object.keys(data))[i]][element][1] > 1) { // надо добавить h-1 пустых строк, чтобы таблица не сломалась(h - высота строки)
                        shablon += `<tr><th  id="time">${time_lst[timer]}</th></tr>`
                        timer += 1 // В первом столбце всегда будет 6 рядов, поэтому каждый раз генерим новую строку для 1 столбца и увеличиваем таймер
                        data[(Object.keys(data))[i]][element][1] -= 1
                    } // уменьшаем высоту уже выбранной строки, чтобы цикл не зациклился
                }
                else { // длинна строки может быть только 1, значит добавляем к шаблону f-строку с заданной высотой
                    shablon += `<td rowspan="1">${data[(Object.keys(data))[i]][element][0]}</td></tr>`
                }
                start += shablon // в конце прибавляем к start сморфированную таблицу
            }
            start += "</tbody></table></div>" // закрываем все теги
        }
        start += "</div></div></div>"
    }
    start += "</div>" // закрываем последний тег
    $('#main-page').append(start) //добавляем таблицу на страничку
};

let weekday_string = ["Вс", "Пн.", "Вт.", "Ср.", "Чт.", "Пт.", "Сб."]

function timeCount() {
    today = new Date()
    let day = today.getDate();
    let month = today.getMonth() + 1;
    let year = today.getFullYear();

    let hour = today.getHours();
    if (hour < 10) hour = "0" + hour;

    let minute = today.getMinutes();
    if (minute < 10) minute = "0" + minute;

    let second = today.getSeconds();
    if (second < 10) second = "0" + second;



    document.getElementById("clock").innerHTML =
        day + "/" + month + "/" + year + " | " + hour + ":" + minute + ":" + second + ` (${weekday_string[today.getDay()]})`;

    setTimeout("timeCount()", 1000);
};