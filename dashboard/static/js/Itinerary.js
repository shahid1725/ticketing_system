// const expensePerson=document.getElementById('expense-person')
// const expenseChild=document.getElementById('expense-child')
// const totalexpense=document.getElementById('total-expense')
// 
// function calculateTotalExpense() {
    // const personValue = parseInt(expensePerson.value) || 0;
    // const childValue = parseInt(expenseChild.value) || 0;
    // const value = personValue + childValue;
// 
    // totalexpense.value = value;
// }
// 
// expensePerson.addEventListener('input', calculateTotalExpense);
// expenseChild.addEventListener('input', calculateTotalExpense);
 
 

const expensePerson = document.getElementById('expense-person');
const personCount = document.getElementById('person-count');
const expenseChild = document.getElementById('expense-child');
const childCount = document.getElementById('child-count');
const totalExpense = document.getElementById('total-expense');


function calculateTotalExpense() {
    const expensePerPerson = parseFloat(expensePerson.value) || 0;
    const numberOfPersons = parseInt(personCount.value) || 1;
    const expensePerChild = parseFloat(expenseChild.value) || 0;
    const numberOfChildren = parseInt(childCount.value) || 1;


    const total = (expensePerPerson * numberOfPersons) + (expensePerChild * numberOfChildren);
    totalExpense.value = total.toFixed(2);
}

expensePerson.addEventListener('input', calculateTotalExpense);
personCount.addEventListener('input', calculateTotalExpense);
expenseChild.addEventListener('input', calculateTotalExpense);
childCount.addEventListener('input', calculateTotalExpense);


document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('flexCheckDefault');
    const singleExpense = document.getElementById('single-expense');
    const splitExpenses = document.getElementById('split-expenses');
    const totalInput = document.querySelector('input[name="total"]');
    const expensePerson = document.getElementById('expense-person');
    const personCount = document.getElementById('person-count');
    const expenseChild = document.getElementById('expense-child');
    const childCount = document.getElementById('child-count');
    const totalExpense = document.getElementById('total-expense');

    function toggleExpenseInputs() {
        if (checkbox.checked) {
            singleExpense.style.display = 'none';
            splitExpenses.style.display = 'block';
            totalInput.required = false;
            expensePerson.required = true;
            expenseChild.required = true;
        } else {
            singleExpense.style.display = 'flex';
            splitExpenses.style.display = 'none';
            totalInput.required = true;
            expensePerson.required = false;
            expenseChild.required = false;
        }
    }

    checkbox.addEventListener('change', toggleExpenseInputs);

    function calculateTotalExpense() {
        const expensePerPerson = parseFloat(expensePerson.value) || 0;
        const numberOfPersons = parseInt(personCount.value) || 1;
        const expensePerChild = parseFloat(expenseChild.value) || 0;
        const numberOfChildren = parseInt(childCount.value) || 1;

        const total = (expensePerPerson * numberOfPersons) + (expensePerChild * numberOfChildren);
        totalExpense.value = total.toFixed(2);
    }

    expensePerson.addEventListener('input', calculateTotalExpense);
    personCount.addEventListener('input', calculateTotalExpense);
    expenseChild.addEventListener('input', calculateTotalExpense);
    childCount.addEventListener('input', calculateTotalExpense);

    // Initial setup
    toggleExpenseInputs();
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



  $(document).ready(function () {
    let counter = 2;
    const maxInputs = 20;
    $("#addInputIcon").click(function () {
        if (counter > maxInputs) {
            alert("You have reached the maximum number of inputs.");
            return;
          }
    const label = counter
    const roomTypeInputName = `visiting_place${counter}`;
    console.log('counter before increment', counter);
    counter++;
    console.log('counter after increment', counter);

      var newInputHtml = `
  <div class="d-flex gap-1 mt-4 position-relative new-input align-items-center">
    <label>Visiting place ${label}:</label>
    <input type="text" class="form-control py-3" placeholder="" name=${roomTypeInputName}>
`;
if ($(".new-input").length > 0) {
    $(".new-input:last").after(newInputHtml);
} else {
    $("#input-container").after(newInputHtml);
}   
    });
  });
  


// activites

  $(document).ready(function () {
    let counter = 2;
    const maxInputs = 5;
    $("#addInputIcon2").click(function () {
        if (counter > maxInputs) {
            alert("You have reached the maximum number of inputs.");
            return;
          }
    const editLabel = counter
    const roomTypeInputName = `extra_activities${counter}`;
    console.log('counter before increment', counter);
    counter++;
    console.log('counter after increment', counter);

      var newInputHtml = `
  <div class="d-flex gap-1 mt-4 position-relative anew-input align-items-center">
    <label>Activity ${editLabel} : </label>
    <input type="text" class="form-control py-3" placeholder="" name=${roomTypeInputName}>
`;
if ($(".anew-input").length > 0) {
    $(".anew-input:last").after(newInputHtml);
} else {
    $("#input-container2").after(newInputHtml);
}   
    });
  });
// 


// edit place
$(document).ready(function () {
    // Initialize counter based on the existing input fields
    let counter = $("input[name^='visiting_place']").length;
    const maxInputs = 20;

    $("#addInputIconEdit").click(function () {
        if (counter >= maxInputs) {
            alert("You have reached the maximum number of inputs.");
            return;
        }
        counter++;
        const roomTypeInputName = `visiting_place${counter}`;
        var newInputHtml = `
            <div class="d-flex gap-2 mt-4 position-relative new-input align-items-center">
                <label>Visiting place ${counter}:</label>
                <input type="text" class="form-control py-3" placeholder="" name="${roomTypeInputName}">
            </div>
        `;
        $("#dynamic-visiting-places-container-edit").append(newInputHtml);

        // Hide the add button if we've reached the maximum
        if (counter >= maxInputs) {
            $("#input-container-edit").hide();
        }
    });
});


//edit activities

$(document).ready(function () {
    // Initialize counter based on the existing input fields
    let counter = $("input[name^='extra_activities']").length;
    const maxInputs = 5;

    $("#addInputIcon2Edit").click(function () {
        if (counter >= maxInputs) {
            alert("You have reached the maximum number of inputs.");
            return;
        }
        counter++;
        const roomTypeInputName = `extra_activities${counter}`;
        var newInputHtml = `
            <div class="d-flex gap-2 mt-4 position-relative anew-input align-items-center">
                <label>Activity ${counter}:</label>
                <input type="text" class="form-control py-3" placeholder="Enter the activities" name="${roomTypeInputName}">
            </div>
        `;
        $("#dynamic-extra-activities-container-edit").append(newInputHtml);

        // Hide the add button if we've reached the maximum
        if (counter >= maxInputs) {
            $("#input-container2-edit").hide();
        }
    });
});

