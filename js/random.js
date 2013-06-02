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
		var row=$(this).parent().parent().parent();
		var input=$(this).parent().parent().parent().find("input");
		if (type == "raw data") type="raw";

		switch(type) {
			case "raw": size="/1024"; break;
			case "string": size="/8"; break;
			default: size="";
		}

		$(input).attr("placeholder","loading...");


		$.getJSON("/api/1/" + type + size, function(data) {
			$(row).find("img").remove();
			$(row).append('<img class="right" src="https://api.qrserver.com/v1/create-qr-code/?data='+data.value+'&size=155x155&margin=12&qzone=2&bgcolor=ffffff&ecc=M" alt="QR Code for random value"/>');
			$(input).val(data.value);
			get_entropy();
		});

		return false;
	});

});
