var algos = {
	"1": "rsa",
	"2": "rsa",
	"3": "rsa",
	"16": "elgamal",
	"17": "dsa",
	"18": "ec",
	"19": "ecdsa",
	"20": "elgamal"
}

function parse_mr_hkp(data, cb) {
	var lines = data.split("\n");
	for(var i=0; i<lines.length; i++) {
		var pub;
		var uid;
		var line = lines[i].split(":");

		switch(line[0]){
			case 'pub':
				if(uid) {
					pub.items.push(uid);
					uid=undefined;
				}
				if(cb&&pub)
					cb(pub)
				pub={
					"type": "pub",
					"items": [],
					"keyid": line[1],
					"algo": algos[line[2]],
					"size": parseInt(line[3]),
					"created": new Date(parseInt(line[4])*1000),
					"expires": line[5]?new Date(parseInt(line[5])*1000):undefined,
					"flags": {
						"revoked": false,
						"disabled": false,
						"expired": false
					}
				}
				if(line[6]){
					if(line[6].indexOf("r")!==-1) pub.flags.revoked = true;
					if(line[6].indexOf("d")!==-1) pub.flags.disabled = true;
					if(line[6].indexOf("e")!==-1) pub.flags.expired = true;
				}

				break;

			case 'uid':
				if(uid) pub.items.push(uid);
				uid={
					"type": "uid",
					"name": line[1],
					"created": new Date(parseInt(line[2])*1000),
					"expires": line[3]?new Date(parseInt(line[3])*1000):undefined,
					"flags": {
						"revoked": false,
						"disabled": false,
						"expired": false
					}
				}

				if(line[4]){
					if(line[4].indexOf("r")!==-1) pub.flags.revoked = true;
					if(line[4].indexOf("d")!==-1) pub.flags.disabled = true;
					if(line[4].indexOf("e")!==-1) pub.flags.expired = true;
				}

				break;
		}

	}
	if(pub&&uid)
		pub.items.push(uid);
	if(cb&&pub)
		cb(pub);


}
function getRepString (rep) {
  rep = rep+''; // coerce to string
  if (rep < 1000) {
    return rep; // return the same number
  } else if (rep < 10000) { // place a comma between
    return rep.charAt(0) + ',' + rep.substring(1);
  } else { // divide and format
  	  if (rep > 1000000) {
  	  	  return  (rep/1000000).toFixed(rep % 1000000 != 0)+'M';
	  }

    return (rep/1000).toFixed(rep % 1000 != 0)+'k';
  }
}

function get_qr_url(key, bgcolor) {
	return "//api.qrserver.com/v1/create-qr-code/?data=http%3A%2F%2Fkeys.connectical.com%2Fpks%2Flookup%3Fop%3Dget%26options%3Dmr%26search%3D0x" + key + "&size=155x155&margin=12&qzone=2&bgcolor=" + bgcolor + "&ecc=M"
}
$(function() {
	$("#add_key .btn-primary").click(function() {
		var form=$(this).parent().parent();
		$.ajax({
			url: $(form).attr("action"),
			type: $(form).attr("method"),
			data: $(form).serialize(),
			success: function(data) {
				$("#add_key").modal('hide');
			},
			error: function(a,b,c) {
				$("#modal_error").html("<span class=\"icon-remove\"></span> Unable to upload the key. Please check that it is a valid OpenPGP armor format.");
			}
		});
		return false;
	});

	$.ajax({
		url: $("#keysh").attr("action") + "?options=mr&op=stats",
		type: "GET",
		success: function(data) {
			var items = $.parseHTML(data);
			$.each(items, function(i,o) {
				if(o.nodeName === "P") {
					var val=$(o).text().split(":")[1]
					if(val)
						$("#total-keys").text(getRepString(val));
				}
			});

			$("#hks_add_new").attr("href", "#add_key");

		},
		error: function(a,b,c) {
			$("#hkp_status").html("<span class=\"icon-warning-sign\"></span> The server has problems. We are working hard to solve it, sorry for the inconvenience.");
			$("#keysh input").attr("disabled","").attr("placeholder", "Disabled due to technical problems");
			$("#keysh button").attr("disabled","").attr("style","background:#888!important");
			$("#hks_add_new").remove();
			return false;
		}
	});

	$("#hkp_search").click(function() {
		var form = $(this).parent().parent();
		var url  = $(form).attr("action") + "?options=mr&" +
				   $(form).serialize();

		$("#results").html(""); // not really safe.

		$.get(url, function(data) {
			parse_mr_hkp(data, function(o) {
				console.log(o);
			var key = $("#key-template").clone().removeClass("hide").attr("id","");
			var bg_color;

			if(o.flags.revoked || o.flags.disabled || o.flags.expired) {
				bg_color="ff9494";
			} else {
				bg_color="dadada";
			}

			$(key).attr("style","background: #" + bg_color + " url('" + get_qr_url(o.keyid, bg_color) + "') no-repeat top right");
			if(o.flags.revoked) $(key).addClass("key-revoked").find(".key-flag").removeClass("hide").html("revoked");
			if(o.flags.disabled) $(key).addClass("key-disabled").find(".key-flag").removeClass("hide").html("disabled");
			if(o.flags.expired) $(key).addClass("key-expired").find(".key-flag").removeClass("hide").html("expired");
			$(key).find(".key-type").html(o.type);
			$(key).find(".key-algo").html(o.algo);
			$(key).find(".key-size").html(o.size);
			$(key).find(".key-id").html("<a href=\"/pks/lookup?op=get&options=mr&search=0x" + o.keyid  + "\">"+ o.keyid+ "</a>");
			$(key).find(".key-created").html("since <b>" + o.created.format("Y-m-d H:i:s P") + "</b>");
			if(o.expires) {
				$(key).find(".key-expires").html("until <b>" + o.expires.format("Y-m-d H:i:s P") + "</b>");
			} else {
				$(key).find(".key-expires").html("and <b>never</b> expires.");
			}
			$(key).find(".key-download a").attr("href", "/pks/lookup?op=get&options=mr&search=0x" + o.keyid);

			$.each(o.items, function(i,u) {
				var uid = $("#key-uid-template").clone().removeClass("hide").attr("id","");
				$(uid).find(".uid-name").text(u.name);
				$(uid).find(".uid-created").html("since <b>" + u.created.format("Y-m-d H:i:s P") + "</b>");
				if(u.expires) {
					$(uid).find(".uid-expires").html("until <b>" + u.expires.format("Y-m-d H:i:s P") + "</b>");
				} else {
					$(uid).find(".uid-expires").html("and <b>never</b> expires.");
				}
				$(key).find(".key-uids").append($(uid));

			});
			$(key).appendTo("#results");
			})
		});

		return false;
	});

});
