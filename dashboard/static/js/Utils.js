const numValue = document.getElementById('num-value').textContent
const itineraryElement = document.getElementById('itinerary-num');
const itnryValue = itineraryElement ? itineraryElement.textContent : 'default-value';

document.getElementById("downloadButton").addEventListener("click", function () {
       const element = document.getElementById("invoice-details");
       const opt = {
           // margin: 0.5,
           filename: `${numValue}.pdf`,
           image: { type: 'jpeg', quality: 1 },
           html2canvas: { scale: 1 },
           jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
       };
       html2pdf().from(element).set(opt).save();
   });

   function printDiv(divId) {
    const divToPrint = document.getElementById(divId);
    const printContents = divToPrint.innerHTML;
    const originalContents = document.body.innerHTML;
  
    // Create a temporary print container for styling consistency:
    const printContainer = document.createElement("div");
    printContainer.style.width = "100%"; // Ensure full width
    printContainer.style.height = "auto"; // Set height to auto for better page height adjustment
    printContainer.style.overflow = "hidden"; // Prevent scrollbars
  
    // Select all divs with the class 'invoice-content'
    const invoiceContentDivs = divToPrint.querySelectorAll(".invoice-content");
  
    // Loop through each 'invoice-content' div
    invoiceContentDivs.forEach((contentDiv, index) => {
      const contentClone = contentDiv.cloneNode(true);
      const tempContainer = document.createElement("div");
      tempContainer.style.pageBreakAfter = "always"; // Add page break after each div
      tempContainer.appendChild(contentClone);
      printContainer.appendChild(tempContainer);
    });
  
    document.body.innerHTML = printContainer.outerHTML;
  
    // Open a new window for printing with portrait layout and 100% height
    const printWindowOptions = "width=1600,height=1131,menubar=no,toolbar=no,location=no,status=no,resizable=no,scrollbars=no";
    const printWindow = window.open("", "_blank", printWindowOptions);
    printWindow.document.open();
    printWindow.document.write(`
      <html>
        <head>
          <title>Print Invoice</title>
          <style>
            /* Paste your inline styles here */
            .view-details {
              background-color: #324969;
              padding: 1rem;
              color: white;
            }
    
            html, body {
              height: 100%;
              margin: 0;
            }
  
            /* Add any CSS styles you need for printing */
            @media print {
              @page {
                size: portrait;
                margin: 0;
              }
            }
               .invoice-content {
                box-shadow: none !important;
              }
  
              .view-details >div table:first-child p,#num-value{
              color:white 
              }
          </style>
        </head>
        <body>
          ${printContainer.outerHTML}
        </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  
    document.body.innerHTML = originalContents;
  }
  
  
  const printButton = document.getElementById("print-btn");
  printButton.addEventListener("click", () => {
    printDiv("invoice-details");
    setTimeout(() => {
      window.location.reload();
    }, 500);
  });


  // function printDiv(divId) {
  //   const divToPrint = document.getElementById(divId);
  //   const printContents = divToPrint.innerHTML;
  
  //   const originalContents = document.body.innerHTML;
  
  //   // Create a temporary print container for styling consistency:
  //   const printContainer = document.createElement("div");
  //   printContainer.style.width = "100%"; // Ensure full width
  //   printContainer.style.height = "100%"; // Ensure full height
  //   printContainer.style.overflow = "hidden"; // Prevent scrollbars
  
  //   // Add both divs to the print container:
  //   const esinContainers = document.querySelectorAll(".invoice-content "); 
  //   console.log('ssdsd',esinContainers); // Select all divs with the class
  //   esinContainers.forEach(container => {
  //     printContainer.appendChild(container.cloneNode(true));  // Clone to avoid modifying the original divs
  //   });
  
  //   document.body.innerHTML = printContainer.outerHTML;
  
  //   window.print();
  
  //   document.body.innerHTML = originalContents;
  // }
  
  // // Example usage:
  // const printButton = document.getElementById("print-btn");
  // printButton.addEventListener("click", () => {
  //   printDiv("invoice-details"); // Replace "myDivToPrint" with the actual ID
  //   setTimeout(() => {
  //     window.location.reload();
  //   }, 500);
  // });


  document.getElementById("downloadButton").addEventListener("click", function () {
    const element = document.getElementById("itinerary-details");
    const opt = {
        // margin: 0.5,
        filename: `${itnryValue}.pdf`,
        image: { type: 'jpeg', quality: 1 },
        html2canvas: { scale: 1.5 },
        jsPDF: { unit: 'in', format: [8.5,12], orientation: 'portrait' },
    };
    html2pdf().from(element).set(opt).save();
});
