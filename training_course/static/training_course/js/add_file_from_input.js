let lesson_file_input = document.querySelector('#add-new-lesson-file'); /* при нажатии на кнопку появляется еще одно input поле */
let lesson_file_place = document.querySelector('.add-lesson-files'); /* Блок inputов */

lesson_file_input.addEventListener('click', function () {
    lesson_file_place.insertAdjacentHTML('beforeend',
    '<div class="form-label add-files">' +
        '<label for="id_files">Выберите файлы: </label>' +
        '<input id="id_files" type="file" name="files" multiple="">' +
    '</div>'
    );
}
);

let task_input = document.querySelector('#add-new-task');
let task_place = document.querySelector('.add-task');

task_input.addEventListener('click', function() {
    task_place.style.display = 'block';
    task_input.style.display = 'none';
}
);

let task_file_input = document.querySelector('#add-new-task-file'); /* при нажатии на кнопку появляется еще одно input поле */
let task_file_place = document.querySelector('.add-task-files'); /* Блок inputов */

task_file_input.addEventListener('click', function () {
    task_file_place.insertAdjacentHTML('beforeend',
    '<div class="form-label add-files">' +
        '<label for="id_task_files">Выберите файлы: </label>' +
        '<input id="id_task_files" type="file" name="task_files" multiple="">' +
    '</div>'
    );
}
);
