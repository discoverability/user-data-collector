function send_traking_telemetry(htmlElement, uuid,rank_shift=0)
{

	const xhr = new XMLHttpRequest();
    var data_ui_tracking_context = decodeURIComponent(htmlElement.getAttribute("data-ui-tracking-context"));
    data_ui_tracking_context["rank"]+=rank_shift
	xhr.open('POST', BASE_URL + '/' + uuid + '/netflix');
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(data_ui_tracking_context);
}

window.addEventListener("load", function f()
{

	chrome.storage.sync.get("uuid", function (obj)
	{

		for (let a of document.querySelectorAll(".ptrack-content"))
		{
			send_traking_telemetry(a, obj.uuid);
		}

		for (let arrow of document.querySelectorAll("span.handle"))
		{
            
			arrow.addEventListener("click", function (elt)
			{
                
				for (let p of elt.target.parentNode.parentNode.querySelectorAll(".slider-item"))
				{
					
					for (let klass of p.classList)
					{
						if (klass.match(new RegExp("slider-item-[0-9]", "g")))
						{
							console.log(p);
							send_traking_telemetry(p.querySelector(".ptrack-content"), obj.uuid);
							break;
						}


					}
				}
			});
		}
	})
}, false);