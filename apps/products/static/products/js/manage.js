// apps/products/static/products/js/manage.js
document.addEventListener('DOMContentLoaded', function() {
    const editFields = document.querySelectorAll('.edit-field');
    const saveButton = document.getElementById('save-manage-changes');

    // Помечаем поле как изменённое
    function markModified(field) {
        field.dataset.modified = 'true';
    }

    // Отмечаем изменения на change
    editFields.forEach(field => {
        field.addEventListener('change', function() {
            markModified(this);
        });
    });

    // Обработчик кнопки "Сохранить изменения"
    if (saveButton) {
        saveButton.addEventListener('click', function() {
            const modifiedFields = document.querySelectorAll('.edit-field[data-modified="true"]');
            if (!modifiedFields.length) return;

            const products = {};

            modifiedFields.forEach(field => {
                const productId = field.dataset.productId;
                if (!products[productId]) {
                    products[productId] = [];
                }
                products[productId].push(field);
            });

            const requests = Object.entries(products).map(([productId, fields]) => {
                const formData = new FormData();
                formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
                fields.forEach(field => {
                    const fieldName = field.dataset.field;
                    let value;
                    if (field.type === 'checkbox') {
                        value = field.checked ? 'true' : 'false';
                    } else {
                        value = field.value;
                    }
                    formData.append(fieldName, value);
                });

                return fetch(`/catalog/manage/update/${productId}/`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        throw new Error(data.message || 'Ошибка обновления');
                    }
                    // Снимаем пометку modified после успешного сохранения
                    fields.forEach(field => {
                        delete field.dataset.modified;
                    });
                });
            });

            Promise.all(requests)
                .then(() => {
                    alert('Изменения сохранены');
                })
                .catch(error => {
                    console.error('Ошибка сохранения:', error);
                    alert('Не удалось сохранить изменения. Обновите страницу.');
                    location.reload();
                });
        });
    }
});