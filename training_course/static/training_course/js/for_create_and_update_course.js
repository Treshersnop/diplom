let time_is_fixed = document.getElementById('id_time_is_fixed');
let admission_days = document.getElementById('admission_days-block');

time_is_fixed.addEventListener('change', function () {
    if (time_is_fixed.checked) {
      admission_days.style.display = "block";
    } else {
      admission_days.style.display = "none";
    }
})
