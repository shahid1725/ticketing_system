// new input
  $(document).ready(function () {
    let counter = 2;
    const maxInputs = 10;
    $("#addInputIcon").click(function () {
        if (counter >= maxInputs) {
            alert("You have reached the maximum number of inputs.");
            return;
          }
    // var inputValue = $("#roomTypeInput").val().trim(); 
    const priceInputName = `price${counter}`;
    const roomTypeInputName = `room_type${counter}`;
    console.log('counter before increment', counter);
    counter++;
    console.log('counter after increment', counter);

      var newInputHtml = `
  <div class="d-flex gap-5">
    <label for=""> Price:</label>
    <div class="input-group">
      <span class="input-group-text" id="basic-addon1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="icon icon-tabler icons-tabler-outline icon-tabler-currency-rupee"
        >
          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
          <path d="M18 5h-11h3a4 4 0 0 1 0 8h-3l6 6" />
          <path d="M7 9l11 0" />
        </svg>
      </span>
      <input
        type="text"
        class="form-control"
        placeholder="Enter Price"
        aria-label="Username"
        aria-describedby="basic-addon1"
        name=${priceInputName}
      />
    </div>
  </div>
  <div class="d-flex gap-5 position-relative">
    <label>Room Type:</label>
    <input type="text" class="form-control" placeholder="" name=${roomTypeInputName}>
  </div>
`;
      $("#input-container").after(newInputHtml); 
    });
  });



  
  

// Amenities---------------------------------------------------------------------------------------------------------------------->
  const addAmenityBtn = document.getElementById('addAmenityBtn');
  const amenitiesDropdown = document.getElementById('amenitiesDropdown');
  const closeBtn = document.getElementById('closeBtn');
  const amenitiesInput = document.getElementById('amenitiesInput');
  let selectedAmenities = [];

  addAmenityBtn.addEventListener('click', () => {
    amenitiesDropdown.style.display = 'block';
  });

  amenitiesDropdown.addEventListener('click', (event) => {
    if (event.target.tagName === 'SPAN') {
      const selectedAmenity = event.target.dataset.value;
      if (event.target.classList.contains('highlight')) {
        // Deselect the highlighted span
        event.target.classList.remove('highlight');
        selectedAmenities = selectedAmenities.filter(amenity => amenity !== selectedAmenity);
      } else {
        // Highlight the span and add its value to the selected amenities
        event.target.classList.add('highlight');
        if (!selectedAmenities.includes(selectedAmenity)) {
          selectedAmenities.push(selectedAmenity);
        }
      }
      amenitiesInput.value = selectedAmenities.join(', ');
    }
  });

  closeBtn.addEventListener('click', () => {
    amenitiesDropdown.style.display = 'none';
  });

//   customfile upload---------------------------------------------------------------------------------------------------------------------->
  document.getElementById("chooseFile").addEventListener("change", function () {
    var filename = this.value;
    if (/^\s*$/.test(filename)) {
      document.querySelector(".file-upload").classList.remove("active");
      document.getElementById("noFile").textContent = "No file chosen...";
    } else {
      document.querySelector(".file-upload").classList.add("active");
      document.getElementById("noFile").textContent = filename.replace(
        "C:\\fakepath\\",
        ""
      );
    }
  });
