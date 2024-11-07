document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');
  const suggestionsList = document.getElementById('suggestions');
  const suggestions = document.querySelectorAll('.suggestion');
  const customerIdInput = document.getElementById('customer_id');
  let timeout;

  searchInput.addEventListener('input', function () {
      const searchTerm = this.value.trim().toLowerCase();

      clearTimeout(timeout);

      if (searchTerm === '') {
          suggestionsList.style.display = 'none';
          return;
      }

      timeout = setTimeout(() => {
          const matchingCustomers = Array.from(suggestions).filter(suggestion => {
              const text = suggestion.textContent.toLowerCase();
              return text.includes(searchTerm);
          });

          if (matchingCustomers.length > 0) {
              suggestionsList.innerHTML = ''; // Clear previous suggestions
              matchingCustomers.forEach(customer => {
                  suggestionsList.appendChild(customer);
              });
              suggestionsList.style.display = 'block';
          } else {
              // If no matching customer found, display "No results found"
              suggestionsList.innerHTML = '<li>No results found</li>';
              suggestionsList.style.display = 'block';
          }
      }, 100); // Adjust the delay time here (in milliseconds)
  });

  // Add click event listener to suggestions
  suggestions.forEach(function (suggestion) {
      suggestion.addEventListener('click', function () {
          searchInput.value = this.firstElementChild.textContent.trim();
          customerIdInput.value = this.getAttribute('data-id');
          suggestionsList.style.display = 'none'; // Clear suggestions after selection
      });
  });
});


document.addEventListener('DOMContentLoaded', function () {
  // For resort search
  const resortSearchInput = document.getElementById('resortSearchInput');
  const resortSuggestionsList = document.getElementById('resortSuggestions');
  const resortSuggestions = document.querySelectorAll('.resort-suggestion');
  const resortIdInput = document.getElementById('resort_id');
  let resortTimeout;

  resortSearchInput.addEventListener('input', function () {
      const searchTerm = this.value.trim().toLowerCase();

      clearTimeout(resortTimeout);

      if (searchTerm === '') {
          resortSuggestionsList.style.display = 'none';
          return;
      }

      resortTimeout = setTimeout(() => {
          const matchingResorts = Array.from(resortSuggestions).filter(suggestion => {
              const text = suggestion.textContent.toLowerCase();
              return text.includes(searchTerm);
          });

          if (matchingResorts.length > 0) {
              resortSuggestionsList.innerHTML = ''; // Clear previous suggestions
              matchingResorts.forEach(resort => {
                  resortSuggestionsList.appendChild(resort);
              });
              resortSuggestionsList.style.display = 'block';
          } else {
              // If no matching resort found, display "No results found"
              resortSuggestionsList.innerHTML = '<li>No results found</li>';
              resortSuggestionsList.style.display = 'block';
          }
      }, 100); // Adjust the delay time here (in milliseconds)
  });

  // Add click event listener to resort suggestions
  resortSuggestions.forEach(function (suggestion) {
      suggestion.addEventListener('click', function () {
          resortSearchInput.value = this.firstElementChild.textContent.trim();
          resortIdInput.value = this.getAttribute('data-id');
          resortSuggestionsList.style.display = 'none'; // Clear suggestions after selection
      });
  });
});


const messages = document.querySelectorAll('.message');


  messages.forEach(message => {
    setTimeout(() => {
      message.remove();
    }, 2000);
  });

const checkinInput = document.getElementById('checkin_date');
const checkoutInput = document.getElementById('checkout_date');
const nightsInput = document.getElementById('number_of_nights');

checkinInput.addEventListener('change', updateNumberOfNights);
checkoutInput.addEventListener('change', updateNumberOfNights);

function updateNumberOfNights() {
  const checkinDate = new Date(checkinInput.value);
  const checkoutDate = new Date(checkoutInput.value);

  const differenceInTime = checkoutDate.getTime() - checkinDate.getTime();

  const numberOfNights = Math.ceil(differenceInTime / (1000 * 3600 * 24));

  nightsInput.value = numberOfNights;
}

const packagePriceInput = document.getElementById("packageprice");
const totalAmountInput = document.getElementById("totalamount");
const resortAmountInput = document.getElementById("rsrtprice");
const travel = document.getElementById("travel")


function calculateTotal() {
  const price = parseFloat(packagePriceInput.value) || 0;
  const resortprice = parseFloat(resortAmountInput.value) || 0;
  // const tprice = parseFloat(travel.value) || 0

  const totalAmount = price
  totalAmountInput.value = totalAmount.toFixed(2);

  // totalAmountInput.value = totalAmount.toFixed(2);
}


//   packagePriceInput.addEventListener("input", calculateTotal);
resortAmountInput.addEventListener("input", calculateTotal);

const profitinput = document.getElementById("profit-inp")
const resortPrice = document.getElementById("rsrtprice")

function calculateprofit() {
  const total = parseFloat(packagePriceInput.value)
  const resort = parseFloat(resortPrice.value)
  // const tcost = parseFloat(travel.value) || 0
  if(!isNaN(total) && !isNaN(resort)){
    const profit = total - resort
    profitinput.value = profit>=0?profit.toFixed(2):'None'
  }else{
    profitinput.value ='None'
  }

}



const receivedPriceInput = document.getElementById("receivedprice")
const pendingPriceInput = document.getElementById("pendingprice")

function calculatePendingPrice() {
  const total = parseFloat(totalAmountInput.value)
  const received = parseFloat(receivedPriceInput.value)

  if (!isNaN(total) && !isNaN(received)) {
    const pending = total - received;


    pendingPriceInput.value = pending >= 0 ? pending : 'None';
} else {
    pendingPriceInput.value = 'None';
    }

}

// const FromNavigo = document.getElementById('Fnavigo')

// function calculatefromnavigo(){
// const navigoprice = parseInt(resortPrice.value) - parseInt(pendingPriceInput.value)
// console.log('s',pendingPriceInput.value);

// FromNavigo.value = navigoprice
// }

receivedPriceInput.addEventListener("input", ()=>{
calculatePendingPrice();
// calculatefromnavigo();
});
resortAmountInput.addEventListener("input", ()=>{
  calculateTotal();
  calculateprofit();
  calculatePendingPrice();
  // calculatefromnavigo();
});

packagePriceInput.addEventListener("input",()=>{
calculateTotal();
  calculateprofit();
  calculatePendingPrice();
  // calculatefromnavigo();
});

travel.addEventListener("input",()=>{
  calculateprofit()
  calculateTotal()
})

