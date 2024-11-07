document.getElementById('toggle-button').addEventListener('click', function() {
  var sidebar = document.querySelector('.app-sidebar');
  var container = document.querySelector('.app-container');
  var button = document.getElementById('toggle-button');
  // Check if the sidebar is currently visible
  var isVisible = sidebar.style.marginLeft !== '-280px';

  if (isVisible) {
      sidebar.style.marginLeft = '-280px';
      container.style.marginLeft = '0';
      container.style.width = '100vw';
      button.style.transform = 'rotate(0deg)';
  } else {
      sidebar.style.marginLeft = '0';
      container.style.marginLeft = '280px';
      container.style.width = 'calc(100vw - 280px)';
      button.style.transform = 'rotate(180deg)';
  }
});

const currentUrl = window.location.href;
const navLinks = document.querySelectorAll(".sidebar-item > li");

navLinks.forEach((item) => {
  const linkUrl = item.querySelector("a").href;
  if (linkUrl === currentUrl) {
    item.classList.add("current");
  } else {
    item.classList.remove("current-page");
  }
});

const documentTypeSelect = document.getElementById("document_type") || null;
const documentLink = document.getElementById("documentLink");

function updateHref() {
  const selectedValue = documentTypeSelect.value;

  if (selectedValue === "Invoice") {
    documentLink.href = "sales/sale_invoice/invoice";
  } else if (selectedValue === "Voucher") {
    documentLink.href = "sales/sale_voucher/voucher";
  } else {
    documentLink.href = "sales/sale_invoice/invoice";
  }
}

documentTypeSelect.addEventListener("change", updateHref);

function preventRefresh(e){
  e.preventDefault()
}

// calendar----------------------------------------------------------------------------------------------------------------------->

const options = {
  settings: {
    visibility: {
      theme: "light",
    },
    selection: {
      // day: false,
      year: false,
    },
  },
  actions: {
    clickDay(event, self,) {
      const clickedDate = self.selectedDates;
      console.log(clickedDate,'date');
      console.log(event.explicitOriginalTarget,'event');
      const today = dayjs().format('YYYY-MM-DD');
      console.log(self,'self');

      const todaysBooking = document.getElementById("todaysBooking");
      if (clickedDate === today) {
        todaysBooking.style.bottom = '-60% ';
      }

      const targetedclass=event.explicitOriginalTarget.querySelector('.vanilla-calendar-day__btn_today.vanilla-calendar-day__btn_selected')
      console.log(targetedclass);
      const cls_btn=document.getElementById('BookingClose')
      cls_btn.addEventListener('click',()=>{
        todaysBooking.style.bottom = '30% ';
        // targetedclass.classList.remove="vanilla-calendar-day__btn_selected"
      })
    },
    // getDays(day, date, HTMLElement, HTMLButtonElement, self) {
    //   const clickedDate = self.selectedDates[0];
    //   const today = dayjs().format('YYYY-MM-DD');
    //   console.log(HTMLButtonElement.outerHTML,'ddddd');
    //   const targetElement =HTMLElement;
    //   const outerHTML = targetElement;

      
    //   // Create a temporary div
    //   const tempDiv = document.createElement('div');
    //   tempDiv.innerHTML = outerHTML;
      
    //   // Select the element with the desired attribute
    //   const selectedElement = tempDiv.querySelector('vanilla-calendar-day__btn_selected');

    //   console.log(selectedElement,'dddd');
      
    //   if (selectedElement) {
    //     const cls_btn=document.getElementById('BookingClose')
    //     cls_btn.addEventListener('click',()=>{
    //       selectedElement.classList.remove('vanilla-calendar-day__btn_selected');
    //     })
    //     // Remove the class
       
      
    //     // Update the target element
    //     const targetChild = targetElement.querySelector(`:scope > ${selectedElement.outerHTML}`);
    //     if (targetChild) {
    //       targetChild.className = selectedElement.className;
    //     }
    //   }
    // },
}
};
// document.addEventListener("DOMContentLoaded", () => {
//   const calendar = new VanillaCalendar("#calendar", options);
//   calendar.init();
// });







// const today2 = dayjs();
// const formattedDay = today2.format('ddd');
// const formattedDate = today2.format('D');

// const day =document.querySelector('#BookingDate >.day')
// const date =document.querySelector('#BookingDate >.date')
// day.textContent = formattedDay
// date.textContent = formattedDate


