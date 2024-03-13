// document.getElementById('generatePdf').addEventListener('click', function () {
//     const content = document.querySelector('.content');

//     // Use html2pdf library to generate PDF
//     html2pdf(content, {
//       margin: 10,
//       filename: 'output.pdf',
//       image: { type: 'jpeg', quality: 0.98 },
//       html2canvas: { scale: 2 },
//       jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
//     });
//   });
  

async function generatePDF() {

    const element = document.getElementById("content");

    // Use html2canvas to render the element as canvas
    const canvas = await html2canvas(element);

    // Create a new jsPDF instance
    const pdf = new jspdf.jsPDF();

    // Add the canvas as an image to the PDF
    const imgData = canvas.toDataURL("image/png");
    pdf.addImage(imgData, 'PNG', 0, 0);

    // Save the PDF
    pdf.save("download.pdf");

}