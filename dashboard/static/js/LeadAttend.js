const decrementBtn = document.getElementById("decrement");
const incrementBtn = document.getElementById("increment");
const quantityInput = document.getElementById("quantity");
const decrementBtn2 = document.getElementById("decrement2");
const incrementBtn2 = document.getElementById("increment2");
const quantityInput2 = document.getElementById("quantity2");

decrementBtn.addEventListener("click", decrementQuantity);
incrementBtn.addEventListener("click", incrementQuantity);
quantityInput.addEventListener("input", handleInputChange);
decrementBtn2.addEventListener("click", decrementQuantity2);
incrementBtn2.addEventListener("click", incrementQuantity2);
quantityInput2.addEventListener("input", handleInputChange2);

// Decrement quantity function
function decrementQuantity() {
  let quantity = parseInt(quantityInput.value);
  if (quantity > 0) {
    quantity--;
    updateQuantity(quantity);
  }
}

function decrementQuantity2() {
  let quantity = parseInt(quantityInput2.value);
  if (quantity > 0) {
    quantity--;
    updateQuantity2(quantity);
  }
}

// Increment quantity function
function incrementQuantity() {
  let quantity = parseInt(quantityInput.value);
  quantity++;
  updateQuantity(quantity);
}

function incrementQuantity2() {
  let quantity = parseInt(quantityInput2.value);
  quantity++;
  updateQuantity2(quantity);
}
// Update the quantity input
function updateQuantity(quantity) {
  quantityInput.value = quantity;
}


function updateQuantity2(quantity) {
  quantityInput2.value = quantity;
}

// Handle input change
function handleInputChange() {
  let quantity = parseInt(quantityInput.value);
  if (isNaN(quantity) || quantity < 1) {
    quantity = 1;
  }
  updateQuantity(quantity);
}
function handleInputChange2() {
  let quantity = parseInt(quantityInput2.value);
  if (isNaN(quantity) || quantity < 1) {
    quantity = 1;
  }
  updateQuantity2(quantity);
}

// select option----------------------------------------------------------------------------->
window.onload = function() {
  const selectElement = document.getElementById('sMinutes');

// Generate 60 options
for (let i = 0; i <= 59; i++) {
  const option = document.createElement('option');
  // Format number with leading zero if less than 10
  const formattedValue = i < 10 ? `0${i}` : `${i}`;
  option.value = formattedValue;  // Set both value and text to the formatted number
  option.textContent = formattedValue;
  selectElement.appendChild(option);
}
};
// Calendar ---------------------------------------------------------------------------------->
const currentMonthElement = document.getElementById("currentMonth");
const daysContainer = document.querySelector(".days");
const daysNameContainer = document.querySelector(".calendar .daysname");
const selectedDateElement = document.getElementById("selectedDate");
const tday = document.querySelector("#BookingDate >.tday");
const date = document.querySelector("#BookingDate >.date");
const currentDay = document.getElementById("today");
const passingDay =document.getElementById("currentDate")

const today = dayjs();
let currentMonth = today;

function renderCalendar() {
  currentMonthElement.textContent = currentMonth.format("MMMM YYYY");
  daysContainer.innerHTML = "";

  const dayAbbreviations = ["S", "M", "T", "W", "T", "F", "S"];

  // Create a row element for the day abbreviations
  const dayAbbrRow = document.createElement("div");
  dayAbbrRow.classList.add("day-abbr-row");

  // Add a div for each day abbreviation
  dayAbbreviations.forEach((abbreviation) => {
    const dayAbbrCell = document.createElement("div");
    dayAbbrCell.textContent = abbreviation;
    dayAbbrCell.classList.add("day-abbr");
    dayAbbrRow.appendChild(dayAbbrCell);
  });

  // Append the row of day abbreviations to the daysname container

  daysNameContainer.innerHTML = "";
  daysNameContainer.appendChild(dayAbbrRow);

  const startOfMonth = currentMonth.startOf("month");
  const endOfMonth = currentMonth.endOf("month");

  // Get the start day of the month (e.g., 0 for Sunday, 1 for Monday, etc.)
  const startDayOfWeek = startOfMonth.day();

  // Calculate the number of days to render before the start of the month
  const daysBeforeStartOfMonth = startDayOfWeek;

  // Render the days before the start of the month (empty placeholders)
  for (let i = 0; i < daysBeforeStartOfMonth; i++) {
    const emptyDayElement = document.createElement("div");
    emptyDayElement.classList.add("empty-day");
    daysContainer.appendChild(emptyDayElement);
  }

  let day = startOfMonth;
  while (day.isBefore(endOfMonth, "day") || day.isSame(endOfMonth, "day")) {
    const dayElement = document.createElement("div");
    dayElement.classList.add("day");
    dayElement.textContent = day.format("D");
    const formattedDay = day.format("ddd");
    const clickedDay = day.format("dddd");
    const clickedDate = day.format("DD-MM-YYYY");
    const currentDate = today.format("DD-MM-YYYY");
    const formattedDate = day.format("D");

    dayElement.addEventListener("click", () => {
      console.log("s", day.isSame(today, "day"));
      console.log(currentDate, "today");
      if (currentDate === clickedDate) {
        console.table(currentDate, clickedDate);
        currentDay.textContent = "Today";
      } else {
        currentDay.textContent = clickedDay;
      }
      tday.textContent = formattedDay;
      date.textContent = formattedDate;
      passingDay.value=clickedDate;
      todaysBooking.style.bottom = "-65%";
    });

    if (day.isSame(today, "day")) {
      dayElement.classList.add("today");
    }

    daysContainer.appendChild(dayElement);
    day = day.add(1, "day");
  }
}

const cls_btn = document.getElementById("BookingClose");
cls_btn.addEventListener("click", () => {
  todaysBooking.style.bottom = "30% ";
});

document.getElementById("prevMonth").addEventListener("click", () => {
  currentMonth = currentMonth.subtract(1, "month");
  renderCalendar();
});

document.getElementById("nextMonth").addEventListener("click", () => {
  currentMonth = currentMonth.add(1, "month");
  renderCalendar();
});

renderCalendar();

const messages = document.querySelectorAll('.message');
  messages.forEach(message => {
    setTimeout(() => {
      message.remove();
    }, 2000);
  });

document.addEventListener("DOMContentLoaded", function() {
            // Check local storage for active tab
            var activeTab = localStorage.getItem('activeTab');
            if (activeTab) {
                var tabButton = document.querySelector('[data-bs-target="' + activeTab + '"]');
                if (tabButton) {
                    var tab = new bootstrap.Tab(tabButton);
                    tab.show();
                }
            }

            // Save the active tab in local storage
            document.querySelectorAll('button[data-bs-toggle="pill"]').forEach(function(tabButton) {
                tabButton.addEventListener('shown.bs.tab', function (e) {
                    localStorage.setItem('activeTab', e.target.getAttribute('data-bs-target'));
                });
            });
        });

        // Ensure the form submission does not reset the tab
        document.querySelectorAll("form").forEach(form => {
            form.addEventListener("submit", function() {
                var activeTab = document.querySelector('.nav-link.active').getAttribute('data-bs-target');
                localStorage.setItem('activeTab', activeTab);
            });
        });



