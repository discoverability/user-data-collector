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

function handle_lolomo(uuid,lolomo_node){
    //regexp used to understand the reason for the lolomo
    var genre_parser_regexp=new RegExp("/browse/([a-zA-Z]+)/([0-9]+)","i");
    //the page lolomo container, used to get this lolomo rank
    var lolomo_container=document.querySelector("div.lolomo");

    //if the lolomo_container is not already present, skip
    if(lolomo_container!=null){
        //type of lolomo
        var lolomo_data_list_context = lolomo_node.getAttribute("data-list-context");
        //rank of the lolomo in the page
        var lolomo_index = Array.prototype.indexOf.call(lolomo_container.children, lolomo_node);

        //when associated with another content, there's a link in the lolomo
        let lolomo_link = lolomo_node.querySelector("h2 a");
        if(lolomo_link!=null){
            //if there's a link
            //extract the full text version of the lolomo
            let lolomo_full_text_title = lolomo_link.getAttribute("aria-label");
            //extract the link to the other content associated with the lolomo
            let lolomo_associated_content_href = lolomo_link.getAttribute("href");
            //extract data for associated content        
            let lolomo_associated_content_data = genre_parser_regexp.exec(lolomo_associated_content_href);
            if(lolomo_associated_content_data==null){
                //we are not able to extract data from the link
                send_tracking_lolomo_telemetry(uuid,lolomo_index,lolomo_data_list_context,"",lolomo_full_text_title);
            }
            else{
            let lolomo_association_type = lolomo_associated_content_data[1];
            let lolomo_associated_content_id = lolomo_associated_content_data[2];
            send_tracking_lolomo_telemetry(uuid,lolomo_index,lolomo_association_type,lolomo_associated_content_id,lolomo_full_text_title);
            }
            
        }
        else if (lolomo_data_list_context=="genre"){
            //special case if lolomot is a genra with no associated link
            let lolomo_full_text_title = lolomo_node.querySelector("h2 span div").innerHTML;

            send_tracking_lolomo_telemetry(uuid,lolomo_index,lolomo_data_list_context,"",lolomo_full_text_title);
        }
        else if(lolomo_data_list_context=="bigRow"){
            //special case if lolomo is a big row: we need to extract the content id from an internal div
            var bigrow=lolomo_node.querySelector("div.ptrack-content");
            var data_ui_tracking_context = JSON.parse(decodeURIComponent(bigrow.getAttribute("data-ui-tracking-context")));
            var video_id=data_ui_tracking_context.video_id;
            //console.log(uuid+":"+lolomo_index+":"+lolomo_data_list_context+":"+video_id+":None");

            send_tracking_lolomo_telemetry(uuid,lolomo_index,lolomo_data_list_context,video_id,"");

        }
        else{
            send_tracking_lolomo_telemetry(uuid,lolomo_index,lolomo_data_list_context,"","");
            
        }
    }
    //handle thumbnail behind the lolomo
    for (let slider of lolomo_node.querySelectorAll(".slider-item")) {
        if (isSliderItemShow(slider)) {
            var tracker = slider.querySelector(".ptrack-content");
            send_traking_suggest_telemetry(tracker, uuid, rank_shift = 0)

        }
    }
    //register click listner when browsing lolomo's content
    for (let handle of lolomo_node.querySelectorAll("span.handle")) {
        handle.addEventListener("click", elt => on_slider_handle_clicked(elt, uuid));
    }

}
function send_tracking_watch_telemetry(uuid){
    
    var payload = netflixWatch_parseWatchData()
    payload["single_page_session_id"]=single_page_session_id;
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

    var single_page_session_id=generateUUID();
    send_single_page_session_telemetry(single_page_session_id);

    //even if user starts watch something (netflix changes the history)
    window.onpopstate = window.history.onpushstate = function(e) {
        console.log(e);
    }

    //load lolomo that are already present
    var lolomo_container = document.querySelector("div.lolomo");
    //check if lolomos are present on the page
    if(lolomo_container!=null){
        //loop on all the lolomos, to extract info
        for(let lolomo of document.querySelector("div.lolomo").children){
            handle_lolomo(obj.uuid,lolomo);
        }
    }

    // identify an element to observe
    var elementToObserve = document.querySelector("body");

    // create a new instance of `MutationObserver` named `observer`, 
    // passing it a callback function
    
    
    var observer = new MutationObserver(function(mutationRecs) {
        //for evry change in the page
        for (let mutation of mutationRecs) {
            //get the new nodes
            for (let addedNode of mutation.addedNodes) {
                //if the new node is a lolomo, handle it
                if (addedNode.classList && addedNode.classList.contains("lolomoRow")) {
                    handle_lolomo(obj.uuid,addedNode);
                } else if (addedNode.classList && addedNode.classList.contains("AkiraPlayer") && addedNode.children.length>0) {
                    //if the new node is a player, handle it
                    if(addedNode.querySelector(".player-loading")==null){
                        send_tracking_watch_telemetry(obj.uuid);
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

    //handle elements that are already present in the page,
    //no dynamically added uppon scrolling

    //the billboard
    var billBoardTracker = document.querySelector(".billboard-row .ptrack-content");
    send_traking_suggest_telemetry(billBoardTracker, obj.uuid);

    //the big rows
    for (let bigrow of document.querySelectorAll(".bigRowItem .ptrack-content")) {
        send_traking_suggest_telemetry(bigrow, obj.uuid);
    }
    //every content already present
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
        var data_ui_tracking_context = JSON.parse(decodeURIComponent(htmlElement.getAttribute("data-ui-tracking-context")));
        data_ui_tracking_context["rank"] += rank_shift
        data_ui_tracking_context["single_page_session_id"]=single_page_session_id;
        xhr.open('POST', BASE_URL + '/' + uuid + '/netflix');
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(data_ui_tracking_context));
    }
}

function send_tracking_lolomo_telemetry(uuid,rank,type,associated_content,full_text_description) {
    
        const xhr = new XMLHttpRequest();
        var payload = new Object();
        payload.rank=rank;
        payload.type=type;
        payload.associated_content=associated_content;
        payload.full_text_description=full_text_description;
        payload.single_page_session_id=single_page_session_id;
        xhr.open('POST', BASE_URL + '/' + uuid + '/netflix/lolomo');
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(payload));
    
}

function send_single_page_session_telemetry(single_page_session){
    const xhr = new XMLHttpRequest();
        var payload = new Object();
        payload.single_page_session=single_page_session;
        payload.width=Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
        payload.height=Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        xhr.open('POST', BASE_URL + '/' + uuid + '/netflix/sps');
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(payload));
}
function on_slider_handle_clicked(elt, uuid) {
    //where the slider is clicked, send the new available nodes if cached
    for (let p of elt.target.parentNode.parentNode.querySelectorAll(".slider-item")) {
        send_traking_suggest_telemetry(p.querySelector(".ptrack-content"), uuid);
    }



}