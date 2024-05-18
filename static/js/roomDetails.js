document.addEventListener('DOMContentLoaded', function() {
    fetchRoomDetails(1, 'room-1');
    fetchRoomDetails(2, 'room-2');
    fetchRoomDetails(3, 'room-3');
    fetchRoomDetails(4, 'room-4');
});

function fetchRoomDetails(roomId, elementId) {
    fetch(`/api/room/${roomId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                renderRoomDetails(data, elementId);
            }
        })
        .catch(error => console.error('Error:', error));
}

function renderRoomDetails(room, elementId) {
    const roomDiv = document.getElementById(elementId);
    let roomHtml = '';

    switch (elementId) {
        case 'room-1':
            roomHtml = `

                <div class="room-details">
                    <h3>Vip room</h3>
                    <p>Просторный номер с видом на город. Включает в себя Wi-Fi и завтрак. ${room.description}</p>
                    <p>Цена за сутки: ${room.price_per_night} рублей</p>
                    <img src="https://yestour.ru/upload/information_system_5/0/1/6/group_16/group_16.jpg" alt="Vip room фото 1">
                    <img src="https://www.thesun.co.uk/wp-content/uploads/2017/12/nintchdbpict000371101827.jpg?strip=all&w=960" alt="Vip room фото 2">
                    <img src="https://www.thesun.co.uk/wp-content/uploads/2017/12/nintchdbpict000371101809.jpg?strip=all&w=960" alt="Vip room фото 3">
                    <a href="/bookings">Перейти к бронированию</a>
                </div>
            `;
            break;
        case 'room-2':
            roomHtml = `
                <h1>Standard Room ${room.room_number}</h1>
                <div class="room-details">
                    <h3>Standard</h3>
                    <p>Уютный номер с собственной ванной комнатой и кондиционером. ${room.description}</p>
                    <p>Цена за сутки: ${room.price_per_night} рублей</p>
                    <img src="https://fb.ru/misc/i/gallery/85188/2662746.jpg" alt="Standard room фото 1">
                    <img src="https://amiel.club/uploads/posts/2022-10/1664841506_14-amiel-club-p-interer-nomera-v-gostinitse-krasivo-15.jpg" alt="Номер 2 фото 2">
                    <img src="https://amiel.club/uploads/posts/2022-10/1664841467_12-amiel-club-p-interer-nomera-v-gostinitse-krasivo-12.jpg" alt="Номер 2 фото 3">
                    <a href="/bookings">Перейти к бронированию</a>
                </div>
            `;
            break;
        case 'room-3':
            roomHtml = `
                <h1>Double Room ${room.room_number}</h1>
                <div class="room-details">
                    <h3>Double room</h3>
                    <p>росторный номер с видом на сад и бассейн. Включает в себя удобства для отдыха и развлечений. ${room.description}</p>
                    <p>Цена за сутки: ${room.price_per_night} рублей</p>
                    <img src="https://www.gannett-cdn.com/-mm-/05b227ad5b8ad4e9dcb53af4f31d7fbdb7fa901b/c=0-64-2119-1259/local/-/media/USATODAY/USATODAY/2014/08/13/1407953244000-177513283.jpg?width=2560" alt="Номер 3 фото 1">
                    <img src="https://amiel.club/uploads/posts/2022-10/1664841552_26-amiel-club-p-interer-nomera-v-gostinitse-krasivo-27.jpg" alt="Номер 3 фото 2">
                    <img src="https://amiel.club/uploads/posts/2022-10/1664841560_35-amiel-club-p-interer-nomera-v-gostinitse-krasivo-36.jpg" alt="Номер 3 фото 3">
                    <a href="/bookings">Перейти к бронированию</a>
                </div>
            `;
            break;
        case 'room-4':
            roomHtml = `
                <h1>Suite Room ${room.room_number}</h1>
                <div class="room-details">
                    <h3>Suite room</h3>
                    <p>Уютный номер с видом на озеро и собственным пляжем. Идеальное место для расслабления у воды. ${room.description}</p>
                    <p>Цена за сутки: ${room.price_per_night} рублей</p>
                    <img src="https://www.cvent.com/sites/default/files/styles/focus_scale_and_crop_800x450/public/image/2021-10/hotel%20room%20with%20beachfront%20view.webp?h=662a4f7c&itok=7Laa3LkQ" alt="Номер 4 фото 1">
                    <img src="https://www.cvent.com/sites/default/files/styles/column_content_width/public/image/2021-10/luxury%20hotel%20room%20bungalow%20with%20bathtub%20overlooking%20ocean_0.jpg?itok=afOVnord" alt="Номер 4 фото 2">
                    <img src="https://amiel.club/uploads/posts/2022-10/1664841523_21-amiel-club-p-interer-nomera-v-gostinitse-krasivo-22.jpg" alt="Номер 4 фото 3">
                    <a href="/bookings">Перейти к бронированию</a>
                </div>
            `;
            break;
    }

    roomDiv.innerHTML = roomHtml;
}
