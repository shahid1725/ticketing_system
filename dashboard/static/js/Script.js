  // Hide messages after 2 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.remove();
        }, 2000);
    });


    function addInput() {
      const container = document.getElementById('input-container');
      const inputCount = container.getElementsByClassName('input-group').length;

      if (inputCount < 6) {
          const newInputGroup = document.createElement('div');
          newInputGroup.className = 'd-flex gap-3 input-group';

          newInputGroup.innerHTML = `
              <label class="align-self-center">Enter Your Script ${inputCount + 1}:</label>
              <input type="text" name="script${inputCount + 1}" class="form-control py-3" placeholder="Enter Your Script${inputCount + 1}">

          `;

          container.appendChild(newInputGroup);
      }else {
        alert('You have exceeded the limit of 6 input fields.');
    }
  }