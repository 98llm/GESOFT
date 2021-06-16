
/**
 * @param {table}
 */
$(document).ready(function () {
    $("#myInput").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});


/**
 * @param {table}
 */

 var table = document.getElementById('table_op');

 var rowLength = table.rows.length;
 
 for(var i=0; i<rowLength; i+=1){
   var row = table.rows[i];
   //your code goes here, looping over every row.
   //cells are accessed as easy
 
   var cellLength = row.cells.length;
   for(var y=0; y<cellLength; y+=1){
     var cell = row.cells[y];
 
     //do something with every cell here
   }
 }
