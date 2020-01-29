function netflixWatch_parseWatchData(){
    var urlParams = new URLSearchParams(window.location.search);
    var payload = new Object();
    payload.track_id=urlParams.get("trackId");
    var video_id=window.location.pathname.split("/")[2];
    payload.video_id=video_id;
    var packedData=urlParams.get("tctx")
    if(packedData){
    packedData=packedData.split(",")
    payload.rank=packedData[0];
    payload.row=packedData[1];
    payload.list_id=packedData[2];
    payload.request_id=packedData[3];
    payload.lolomo_id=packedData[4];
    
    }

    
    return payload;
}
function netflixWatch_onWatching(uuid){
    
    var payload = netflixWatch_parseWatchData()

    const xhr = new XMLHttpRequest();
    xhr.open('POST', BASE_URL + '/' + uuid + '/netflix/watch/'+payload.video_id);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(payload));

}

function isSliderItemShow(slider) {
    for (let klass of slider.classList) {
        if (klass.match(new RegExp("slider-item-[0-9]", "g"))) {
            return true;
        }
    }
    return false;
}

function netflixSuggest_onUUID_loaded(obj) {

    //even if user starts watch something (netflix changes the history)

    window.onpopstate = window.history.onpushstate = function(e) {
        console.log(e);
    }

    // identify an element to observe
    var elementToObserve = document.querySelector("body");

    // create a new instance of `MutationObserver` named `observer`, 
    // passing it a callback function
    var observer = new MutationObserver(function(mutationRecs) {
        for (let mutation of mutationRecs) {
            for (let addedNode of mutation.addedNodes) {

                if (addedNode.classList && addedNode.classList.contains("lolomoRow")) {
                    for (let slider of addedNode.querySelectorAll(".slider-item")) {
                        if (isSliderItemShow(slider)) {
                            var tracker = slider.querySelector(".ptrack-content");
                            send_traking_suggest_telemetry(tracker, obj.uuid, rank_shift = 0)

                        }
                    }
                    for (let handle of addedNode.querySelectorAll("span.handle")) {
                        handle.addEventListener("click", elt => on_slider_handle_clicked(elt, obj.uuid));
                    }


                } else if (addedNode.classList && addedNode.classList.contains("AkiraPlayer") && addedNode.children.length>0) {
                    if(addedNode.querySelector(".player-loading")==null){
                        netflixWatch_onWatching(obj.uuid);
                    }
                    else{
                        //just loading the player, wait for the real Akira to arrive
                    }
                    
                    
                    

                }

            }
        }
    });

    observer.observe(elementToObserve, {
        subtree: true,
        childList: true
    });


    var billBoardTracker = document.querySelector(".billboard-row .ptrack-content");
    send_traking_suggest_telemetry(billBoardTracker, obj.uuid);

    for (let bigrow of document.querySelectorAll(".bigRowItem .ptrack-content")) {
        send_traking_suggest_telemetry(bigrow, obj.uuid);
    }


    for (let slider of document.querySelectorAll(".slider-item")) {
        if (isSliderItemShow(slider)) {
            var tracker = slider.querySelector(".ptrack-content");
            send_traking_suggest_telemetry(tracker, obj.uuid, rank_shift = 0);

        }
    }

    for (let arrow of document.querySelectorAll("span.handle")) {

        arrow.addEventListener("click", elt => on_slider_handle_clicked(elt, obj.uuid));
    }

}

function send_traking_suggest_telemetry(htmlElement, uuid, rank_shift = 0) {
    if (htmlElement) {
        const xhr = new XMLHttpRequest();
        var data_ui_tracking_context = decodeURIComponent(htmlElement.getAttribute("data-ui-tracking-context"));
        data_ui_tracking_context["rank"] += rank_shift
        xhr.open('POST', BASE_URL + '/' + uuid + '/netflix');
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(data_ui_tracking_context);
    }
}

function on_slider_handle_clicked(elt, uuid) {

    for (let p of elt.target.parentNode.parentNode.querySelectorAll(".slider-item")) {

        send_traking_suggest_telemetry(p.querySelector(".ptrack-content"), uuid);



    }



}