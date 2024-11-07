const currentMonthElement = document.getElementById("currentMonth");
const daysContainer = document.querySelector(".days");
const daysNameContainer = document.querySelector(".calendar .daysname");
const selectedDateElement = document.getElementById("selectedDate");
const tday = document.querySelector("#BookingDate >.tday");
const date = document.querySelector("#BookingDate >.date");
const currentDay = document.getElementById("today");
const bookingwrapper = document.getElementById("booking-data-wrapper")
const loadingElement = document.getElementById("loader-wrapper");
const bookingCount = document.getElementById("bookingCount")

const today = dayjs();
let currentMonth = today;
let bookings = [];

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

    const bookingsOnThisDay = bookings.filter(post => {
      const interviewDate = post['checkin_date'] || ''; // Handle null or undefined values
      const formattedInterviewDate = dayjs(interviewDate, 'YYYY-MM-DD').format('DD-MM-YYYY'); // Convert date format if needed
      return formattedInterviewDate === clickedDate;
    });

    if (bookingsOnThisDay.length > 0) {
      dayElement.classList.add("has-interview");
    }


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

      bookingwrapper.innerHTML='';
      if ( bookingsOnThisDay.length === 0) {
        const noBookingsElement = document.createElement("div");
        bookingCount.textContent = 0
        noBookingsElement.classList.add("no-interview");
        noBookingsElement.textContent = "No Bookings today";
        noBookingsElement.style.textAlign="center"
        bookingwrapper.appendChild(noBookingsElement);
      } else {
        bookingsOnThisDay.forEach(booking => {
        bookingCount.textContent = bookingsOnThisDay.length
        const bookingElement = document.createElement("div");
        bookingElement.classList.add("interview-detail");
        bookingElement.innerHTML = `

          <div class="d-flex justify-content-between mb-2">
            <h3 class="fs-7 fw-semibold">${booking.customer}</h3>
            <a href="sales/sale_invoice/view_invoice/${booking.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none"
                             stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                             class="icon icon-tabler icons-tabler-outline icon-tabler-chevron-right rounded-circle border p-1 align-self-center ms-auto">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M9 6l6 6l-6 6"/>

                        </svg>
                    </a>
          </div>
          <div class="d-flex justify-content-between gap-2">
            <p class="fs-9">Resort: ${booking.resort_name}</p>

          </div>
          <div class="d-flex justify-content-between gap-2">
            <p class="fs-9">Checkin Date: ${booking.checkin_date}</p>
            <p class="fs-9">Checkin Time: ${booking.checkin_time}</p>
          </div>
        `;
        bookingwrapper.appendChild(bookingElement);
      });
     }
      todaysBooking.style.bottom = "-72%";
      
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

loadingElement.style.display = "block";

const origin = window.location.origin; 
console.log('or',origin);

fetch(`${origin}/api/invoices/own_resort/`)
  .then(response => response.json())
  .then(data => {
    bookings = data;
    renderCalendar();
  })
  .catch(error => console.error('Error fetching Booking posts:', error)).finally(() => {
    loadingElement.style.display = "none";
  });;


