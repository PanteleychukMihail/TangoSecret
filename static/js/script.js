document.addEventListener("DOMContentLoaded", function () {
                // Получаем значение уровня из формы
                let levelRadio = document.querySelector('input[name="level"]:checked');
                sortStudents(levelRadio.value);

                // Слушаем изменения уровня в форме
                let levelRadios = document.querySelectorAll('input[name="level"]');
                for (let i = 0; i < levelRadios.length; i++) {
                    levelRadios[i].addEventListener("change", function () {
                        sortStudents(this.value);
                    });
                }
                // Функция сортировки списка студентов
                function sortStudents(level) {
                    let studentsList = document.querySelector('#id_students');
                    if (level === 'beginner') {
                        studentsList.innerHTML = [...studentsList.children].reverse().map(el => el.outerHTML).join('');
                    }
                    if (level !== 'beginner') {
                        studentsList.innerHTML = [...studentsList.children].reverse().map(el => el.outerHTML).join('');
                    }
                }
            }
        );

