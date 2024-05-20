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


        // Simulate hostel occupancy (between 0 and 1)
        var hostelOccupancy = Math.random(); // Generate a random number between 0 and 1

        // Calculate discount based on hostel occupancy
        if (hostelOccupancy < 0.35) {  // Less than 35% occupancy
            discount = 0.14;
        } else if (hostelOccupancy < 0.5) {  // Less than 50% occupancy but more than or equal to 35%
            discount = 0.07;
        } else {  // 50% or more occupancy
            discount = 0.0;
        }


        // Apply discount based on duration
        if (durationInDays > 5 && durationInDays <= 10) {
            discount += 0.03;
        } else if (durationInDays > 10) {
            discount += 0.07;
        }

        // Discount for high number of guests
        if (guests > 3) {
            discount += 0.02;
        }

        // Check if it's a holiday period (for demonstration purposes, let's assume December as Christmas)
        if (new Date().getMonth() === 12) {  // December (0-based index, 11 is December)
            discount += 0.05;
        }

        // Ensure the maximum discount does not exceed 20%
        if (discount > 0.17) {
            discount = 0.17;
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