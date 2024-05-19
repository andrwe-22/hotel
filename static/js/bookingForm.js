/// bookingForm.js ///

function changeImage() {
    var roomSelect = document.getElementById("room");
    var images = document.getElementsByClassName("room-image");

    for (var i = 0; i < images.length; i++) {
        images[i].style.display = "none"; // Hide all images
    }

    var selectedRoom = roomSelect.options[roomSelect.selectedIndex].text;
    if (selectedRoom === "vip room") {
        document.getElementById("room1Image").style.display = "block"; // Show image for room 1
    } else if (selectedRoom === "Standard room") {
        document.getElementById("room2Image").style.display = "block"; // Show image for room 2
    } else if (selectedRoom === "Double room") {
        document.getElementById("room3Image").style.display = "block"; // Show image for room 3
    } else if (selectedRoom === "Suite room") {
        document.getElementById("room4Image").style.display = "block"; // Show image for room 4
    }
    // Add more conditions for other rooms if needed
    calculatePrice(); // Calculate price when room changes
}

function calculatePrice() {
    var checkIn = document.getElementById("check-in").value;
    var checkOut = document.getElementById("check-out").value;
    var guests = document.getElementById("guests").value;
    var roomSelect = document.getElementById("room");
    var selectedRoom = roomSelect.options[roomSelect.selectedIndex].text;

    // Проверка заполнения всех обязательных полей формы
    if (checkIn && checkOut && guests && selectedRoom) {
        var pricePerNight = parseInt(roomSelect.options[roomSelect.selectedIndex].getAttribute("data-price-per-night"));
        var durationInDays = Math.ceil((new Date(checkOut) - new Date(checkIn)) / (1000 * 60 * 60 * 24));
        var totalPrice = durationInDays * pricePerNight * guests;
        var discount = 0.0; // Default discount is 0%

        // Apply additional pricing rules based on the duration of stay
        if (durationInDays > 5 && durationInDays <= 10) {
            // Apply a 5% discount for stays longer than 5 days but less than or equal to 10 days
            discount = 0.05;
        } else if (durationInDays > 10) {
            // Apply a 10% discount for stays longer than 10 days
            discount = 0.10;
        }

        totalPrice -= totalPrice * discount; // Apply the discount

        if (!isNaN(totalPrice)) {
            document.getElementById("priceInfo").textContent = "Стоимость: " + totalPrice.toFixed(2) + " рублей";
            document.getElementById("priceInfo").style.display = "block";
        } else {
            document.getElementById("priceInfo").style.display = "none";
        }

        var guestNamesDiv = document.getElementById("guestNames");
        guestNamesDiv.innerHTML = "";

        for (var i = 1; i <= guests; i++) {
            var label = document.createElement("label");
            label.for = "guest" + i;
            label.textContent = "ФИО гостя " + i + ":";
            guestNamesDiv.appendChild(label);

            var input = document.createElement("input");
            input.type = "text";
            input.id = "guest" + i;
            input.name = "guest" + i;
            input.required = true;
            guestNamesDiv.appendChild(input);

            guestNamesDiv.appendChild(document.createElement("br"));
        }
        // Call function to update the price on room change
        updateBookingPrice();
    } else {
        // Если какие-то поля не заполнены, скрываем цену
        document.getElementById("priceInfo").style.display = "none";
    }
}