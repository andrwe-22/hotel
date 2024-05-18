//  room.js ///

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
                <img loading="lazy" decoding="async" class="ls-is-cached lazyloaded" src="https://yestour.ru/upload/information_system_5/0/1/6/group_16/group_16.jpg">
                <h3><a href="/viproom">Vip Room ${room.room_number}</a></h3>
                <p> Просторный номер с видом на город. Включает в себя Wi-Fi и завтрак.  ${room.description}</p>
                <p>Цена за сутки: ${room.price_per_night} рублей</p>
            `;
            break;
        case 'room-2':
            roomHtml = `
                <img loading="lazy" decoding="async" class="ls-is-cached lazyloaded" data-src="https://fb.ru/misc/i/gallery/85188/2662746.jpg" src="https://fb.ru/misc/i/gallery/85188/2662746.jpg">
                <h3><a href="/Standardroom">Standard room ${room.room_number}</a></h3>
                <p>Уютный номер с собственной ванной комнатой и кондиционером.  ${room.description}</p>
                <p>Цена за сутки: ${room.price_per_night} рублей</p>
            `;
            break;
        case 'room-3':
            roomHtml = `
                <img loading="lazy" decoding="async" src="https://www.gannett-cdn.com/-mm-/05b227ad5b8ad4e9dcb53af4f31d7fbdb7fa901b/c=0-64-2119-1259/local/-/media/USATODAY/USATODAY/2014/08/13/1407953244000-177513283.jpg?width=2560" alt="Double room">
                <h3><a href="/Doubleroom">Double Room ${room.room_number}</a></h3>
                <p> росторный номер с видом на сад и бассейн. Включает в себя удобства для отдыха и развлечений. ${room.description}</p>
                <p>Цена за сутки:  ${room.price_per_night} рублей</p>
            `;
            break;
        case 'room-4':
            roomHtml = `
                <img loading="lazy" decoding="async" src="https://www.cvent.com/sites/default/files/styles/focus_scale_and_crop_800x450/public/image/2021-10/hotel%20room%20with%20beachfront%20view.webp?h=662a4f7c&itok=7Laa3LkQ" alt="Suite room">
                <h3><a href="/Suiteroom">Suite Room ${room.room_number}</a></h3>
                <p>Уютный номер с видом на озеро и собственным пляжем. Идеальное место для расслабления у воды. ${room.description}</p>
                <p>Цена за сутки: ${room.price_per_night} рублей</p>
            `;
            break;
    }

    roomDiv.innerHTML = roomHtml;
}
