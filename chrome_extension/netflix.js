function isSliderItemShow(slider){
    for (let klass of slider.classList)
    {
        if (klass.match(new RegExp("slider-item-[0-9]", "g")))
        {
            
            return true;
        }


    }

    return false;
    
}

function onUUID_loaded(obj)
{


		
        
        // identify an element to observe
var elementToObserve = document.querySelector("body");

// create a new instance of `MutationObserver` named `observer`, 
// passing it a callback function
var observer = new MutationObserver(function(mutationRecs) {
    for(let mutation of mutationRecs){
        for(let addedNode of mutation.addedNodes){
            
            if( addedNode.classList.contains("lolomoRow")){
                for(let slider of addedNode.querySelectorAll(".slider-item")){
                    if(isSliderItemShow(slider)){
                        var tracker = slider.querySelector(".ptrack-content");
                        send_traking_telemetry(tracker, obj.uuid,rank_shift=0)

                    }
                }
                for(let handle of addedNode.querySelectorAll("span.handle")){
                    handle.addEventListener("click", elt => on_handle_clicked(elt,obj.uuid));
                }

                
            }

        }
    }
});

// call `observe` on that MutationObserver instance, 
// passing it the element to observe, and the options object
observer.observe(elementToObserve, {subtree: true, childList: true});


for (let slider of document.querySelectorAll(".slider-item"))
		{
            if(isSliderItemShow(slider)){
                var tracker = slider.querySelector(".ptrack-content");
                send_traking_telemetry(tracker, obj.uuid,rank_shift=0)

            }
		}

		for (let arrow of document.querySelectorAll("span.handle"))
		{
            
			arrow.addEventListener("click", elt => on_handle_clicked(elt,obj.uuid));
        }

}

function send_traking_telemetry(htmlElement, uuid,rank_shift=0)
{

	const xhr = new XMLHttpRequest();
    var data_ui_tracking_context = decodeURIComponent(htmlElement.getAttribute("data-ui-tracking-context"));
    data_ui_tracking_context["rank"]+=rank_shift
	xhr.open('POST', BASE_URL + '/' + uuid + '/netflix');
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log("miom " + data_ui_tracking_context);
	xhr.send(data_ui_tracking_context);
}

function on_handle_clicked(elt,uuid){
    
	 	for (let p of elt.target.parentNode.parentNode.querySelectorAll(".slider-item"))
    {
       
            send_traking_telemetry(p.querySelector(".ptrack-content"), uuid);
       

    
    } 
                
			

}

window.addEventListener("load", function f()
{
    chrome.storage.sync.get("uuid", onUUID_loaded)
}, false);