const checkinInput = document.getElementById("checkin_date");
const checkoutInput = document.getElementById("checkout_date");
const nightsInput = document.getElementById("number_of_nights");

checkinInput.addEventListener("change", updateNumberOfNights);
checkoutInput.addEventListener("change", updateNumberOfNights);

function updateNumberOfNights() {
  const checkinDate = new Date(checkinInput.value);
  const checkoutDate = new Date(checkoutInput.value);

  const differenceInTime = checkoutDate.getTime() - checkinDate.getTime();

  const numberOfNights = Math.ceil(differenceInTime / (1000 * 3600 * 24));

  nightsInput.value = numberOfNights;
}


const packagePriceInput = document.getElementById("packageprice");
// const taxSelect = document.getElementById("tax");
const totalAmountInput = document.getElementById("totalamount");
const guideAmountInput = document.getElementById("guidecharge");
const transportationInput = document.getElementById("transportation")
const otherinput=document.getElementById("other")
const Accomodation=document.getElementById("accomodation")

function calculateTotal() {
  const price = parseFloat(packagePriceInput.value) || 0;
//   const taxRate = parseFloat(taxSelect.value) || 0;
  // const tprice = parseFloat(travel.value) || 0

//   const resortprice = parseFloat(resortAmountInput.value) || 0;

  const Amount = price
  const totalAmount= Amount
  totalAmountInput.value = totalAmount.toFixed(2);


  // const grandtotalp = totalAmount + resortprice;
  // totalAmountInput.value = grandtotalp.toFixed(2);
  // console.log(resortprice,totalAmount, GrandAmountInput.value)
}


// Trigger calculation initially and on changes
packagePriceInput.addEventListener("input", calculateTotal);

guideAmountInput.addEventListener("input", calculateTotal);
//   resortAmountInput.addEventListener("input", GrandTotal);

//   packagePriceInput.addEventListener("input", calculateTotal);
// taxSelect.addEventListener("change", calculateTotal);

const profitinput = document.getElementById("profit-inp")
const resortPrice = document.getElementById("rsrtprice")

function calculateprofit(){
      const total = parseFloat(packagePriceInput.value)
      const guide  = parseFloat(guideAmountInput.value)
      const transportation  = parseFloat(transportationInput.value)
      const accomodation = parseFloat(Accomodation.value)
      const other = parseFloat(otherinput.value)
      // const tcost = parseFloat(travel.value) || 0

      if(!isNaN(total) && !isNaN(guide)){
        const profit = total -transportation - accomodation - guide -other
        profitinput.value = profit>=0?profit.toFixed(2):'None'
      }else{
        profitinput.value ='None'
      }



      console.log('dd')
}

// resortAmountInput.addEventListener("input",calculateprofit);


const receivedPriceInput = document.getElementById("receivedprice")
const pendingPriceInput = document.getElementById("pendingprice")

function calculatePendingPrice(){
  const total = parseFloat(totalAmountInput.value)
  const received = parseFloat(receivedPriceInput.value)

  if (!isNaN(total) && !isNaN(received)) {
      const pending = total - received;

      // Update the pending price input value
      pendingPriceInput.value = pending >= 0 ? pending : 'None';
  } else {
      // If any input value is not a valid number, show 'None' in the pending price input
      pendingPriceInput.value = 'None';
    }

  // pendingPriceInput.value = pending
}

// const FromNavigo = document.getElementById('Fnavigo')

// function calculatefromnavigo(){
//   const navigoprice = parseInt(resortPrice.value) - parseInt(pendingPriceInput.value)
//   console.log('s',pendingPriceInput.value);

//   FromNavigo.value = navigoprice
// }

receivedPriceInput.addEventListener("input", ()=>{
  calculatePendingPrice();
  // calculatefromnavigo()
});

packagePriceInput.addEventListener("input",()=>{
calculateTotal();
      calculateprofit();
      calculatePendingPrice();
      // calculatefromnavigo();
    });

// taxSelect.addEventListener("change", ()=>{
//       calculateTotal();
//       calculateprofit();
//       calculatePendingPrice();
//       // calculatefromnavigo()
//     });


otherinput.addEventListener("input", ()=>{
    calculateprofit();
  });
  
Accomodation.addEventListener("input", ()=>{
    calculateprofit();
  });

transportationInput.addEventListener("input", ()=>{
    calculateprofit();
  });

guideAmountInput.addEventListener("input",()=>{
  calculateTotal();
  calculateprofit();
  calculatePendingPrice()
});




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