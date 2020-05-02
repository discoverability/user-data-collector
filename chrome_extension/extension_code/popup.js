'use strict';

chrome.storage.sync.get("uuid", function (obj) {
  document.getElementById('uuidCreated').innerText = obj.uuid;
  document.querySelector("#logslink a").onclick = function () {
    chrome.tabs.create({active: true, url: BASE_URL+"/"+obj.uuid});
  };

 
});
