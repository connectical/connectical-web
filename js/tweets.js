function getGithubActivity(user) {
	$.ajax({
		url: "https://api.github.com/users/" + user + "/events",
		type: 'GET',
		dataType: 'JSONP',
		success: function(data) {
			console.log(data)
			$.each(data.data.filter(function(o) {
				return o.type == "PushEvent";
			}), function(i,o) {
				var code = $("#post-ghactivity-tpl").clone().attr('id','');
				$(code).find(".entry-author").html(
					'<a href="https://github.com/' + o.actor.login + '">' + o.actor.login + "</a>");
				$(code).find(".entry-date").html(o.created_at.split("T")[0]);
				$.each(o.payload.commits, function(i,o2) {
					$(code).find("dl").append('<dt><a href="' + o2.url + '">Commit #' + o2.sha.slice(0,8) + '</a> at <a href="' + o.repo.url +'">' + o.repo.name + "</a></dt>" +
						'<dd>' + o2.message + '</dd>');
				});
				$(code).appendTo("#bitems").removeClass("hide");
				$("article").sortElements(function(a,b) {
					a = $(a).find(".entry-date").html();
					b = $(b).find(".entry-date").html();
					return (a<b)?1:((a==b)?0:-1);
				});
			});
		}
	});
}
