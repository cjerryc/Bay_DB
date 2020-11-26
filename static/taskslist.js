//VV this doesnt work because for some reason, because we are using a for loop to find our tasks, the tasks are not identifiable
// by value....

// highlight_row();
// function highlight_row() {
//     var table = document.getElementById('tblSearch');
//     var cells = table.getElementsByTagName('td');
//     console.log(cells);
//     for (var i = 0; i < cells.length; i++) {
//         // Take each cell
//         var cell = cells[i];
//         // do something on onclick event for cell
//         cell.onclick = function () {
//             // Get the row id where the cell exists
//             var rowId = this.parentNode.rowIndex;

//             var rowsNotSelected = table.getElementsByTagName('tr');
//             for (var row = 0; row < rowsNotSelected.length; row++) {
//                 rowsNotSelected[row].style.backgroundColor = "";
//                 rowsNotSelected[row].classList.remove('selected');
//             }
//             var rowSelected = table.getElementsByTagName('tr')[rowId];
//             rowSelected.style.backgroundColor = "yellow";
//             rowSelected.className += " selected";

//             msg = 'The ID of the company is: ' + rowSelected.cells[0].innerHTML;
//             msg += '\nThe cell value is: ' + this.innerHTML;
//             console.log(msg);
//         }
//     }
// }
// function myFunction() {
//     var table = document.getElementByTagName('tblSearch');
//     document.getElementById("taaDaa").innerHTML = "did this work" + table;
//   }


function descriptionsView() {
    var x = document.getElementById("taaDaa");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    } 
}

