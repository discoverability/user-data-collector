function generatedUuid() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    )
}

chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.sync.set({uuid: generatedUuid()});
  chrome.storage.sync.get("uuid", function (obj) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', BASE_URL+"/"+obj.uuid);
    xhr.send();
  })
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([{
      conditions: [new chrome.declarativeContent.PageStateMatcher({
        
      })
      ],
          actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
  });


  


});
