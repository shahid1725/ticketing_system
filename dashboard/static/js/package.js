  // Hide messages after 2 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.remove();
        }, 2000);
    });

    // Function to show trip details and hide stay details
    function showTripDetails() {
        document.getElementById('trip-details').style.display = 'block';
        document.getElementById('stay-details').style.display = 'none';
        document.getElementById('details-select').value = '1';
    }
    
    function showStayDetails() {
        document.getElementById('trip-details').style.display = 'none';
        document.getElementById('stay-details').style.display = 'block';
        document.getElementById('details-select').value = '2';
    }
    
    document.getElementById('details-select').addEventListener('change', function() {
        if (this.value == '1') {
            showTripDetails();
        } else if (this.value == '2') {
            showStayDetails();
        }
    });
    
    // Check URL parameters to decide which details to show
    function checkURLParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const show = urlParams.get('show') || urlParams.get('stay_q');
        if (show) {
            showStayDetails();
        } else {
            showTripDetails();
        }
    }
    
    // Call this function when the page loads
    window.onload = checkURLParams;


    // function checkURLParams2(){
    //     const urlParams = new URLSearchParams(window.location.search)

    //     const show = 
    // }

    