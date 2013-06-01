function get_entropy() {
	$.ajax({
		url: "/api/1/entropy",
		type: "GET",
		dataType: "JSON",
		success: function(data) {
				$("#total-entropy").html(data.buf_items);

		},
		error: function(a,b,c) {
			$("#rng_status").html("<span class=\"icon-warning-sign\"></span> The server has problems. We are working hard to solve it, sorry for the inconvenience.");
			return false;
		}
	});
}

$(function() {

	get_entropy();

	$("#produce button").click(function() {
		var type=$(this).text().toLowerCase();
		var input=$(this).parent().parent().parent().find("input");
		if (type == "raw data") type="raw";

		switch(type) {
			case "raw": size="/1024"; break;
			case "string": size="/8"; break;
			default: size="";
		}

		$(input).attr("placeholder","loading...");


		$.getJSON("/api/1/" + type + size, function(data) {
			$(input).val(data.value);
			get_entropy();
		});

		return false;
	});

});
