$( document ).ready(function() {

	//Tables Values
	var counter = 0;
	counter = $('#moreFieldsTable tr').length - 2;

	$("#addrow").on("click", function () {
		
		var newRow = $("<tr>");
		var cols = "";
		cols += '<td><input type="checkbox" name="check"></td>';
		cols += '<td><input style="width:180px" type="text" name="name" /></td>';
		cols += '<td><input style="width:70px" type="text" name="centro"/></td>';
		cols += '<td><input style="width:70px" type="text" name="leste"/></td>';
		cols += '<td><input style="width:70px" type="text" name="norte"/></td>';
		cols += '<td><input style="width:70px" type="text" name="oeste"/></td>';
		cols += '<td><input style="width:70px" type="text" name="sudeste"/></td>';
		cols += '<td><input style="width:70px" type="text" name="sul"/></td>';
		cols += '<td><a class="deleteRow"></a></td>';
		newRow.append(cols);
		
		$("#moreFieldsTable").append(newRow);
		counter++;
	});

	function tableModify(){
		var lista = [];
		var MyRows = $('#moreFieldsTable').find('tbody').find('tr');

		for (var i = 0; i < MyRows.length; i++) {
			if ($(MyRows[i]).find('td:eq(0)').children().is(':checked')){

				var item = {};

				if ($(MyRows[i]).find('td:eq(1)').children().val() != undefined){
					item = {
						'field' : $(MyRows[i]).find('td:eq(1)').children().val(),
						'centro' : $(MyRows[i]).find('td:eq(2)').children().val(),
						'leste' : $(MyRows[i]).find('td:eq(3)').children().val(),
						'norte' : $(MyRows[i]).find('td:eq(4)').children().val(),
						'oeste' : $(MyRows[i]).find('td:eq(5)').children().val(),
						'sudeste' : $(MyRows[i]).find('td:eq(6)').children().val(),
						'sul' : $(MyRows[i]).find('td:eq(7)').children().val()
					};
				} else{
					item = {
						'field' : $(MyRows[i]).find('td:eq(1)').text(),
						'centro' : $(MyRows[i]).find('td:eq(2)').text(),
						'leste' : $(MyRows[i]).find('td:eq(3)').text(),
						'norte' : $(MyRows[i]).find('td:eq(4)').text(),
						'oeste' : $(MyRows[i]).find('td:eq(5)').text(),
						'sudeste' : $(MyRows[i]).find('td:eq(6)').text(),
						'sul' : $(MyRows[i]).find('td:eq(7)').text()
					};
				}

				
				lista.push(item);
			}
		}

		$('#moreFieldsInput').val(JSON.stringify(lista));
	}

	$("#moreFieldsTable").on("change", function (event) {
		tableModify();
	});

	$("#moreFieldsTable").on("click", "#ibtnDel", function (event) {
		$(this).closest("tr").remove();
		counter --;
	});

	tableModify();

	// $(function() {
		
	// });


});