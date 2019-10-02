// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

/**
 * Listens for the app launching then creates the window
 *
 * @see http://developer.chrome.com/apps/app.window.html
 */

chrome.runtime.onInstalled.addListener(function (details) {
  if (details.reason == "install") {
    chrome.app.window.create('options.html', {
      id: 'options',
      bounds: {
        width: 1024,
        height: 768
      }
    });
  }
});

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
  chrome.storage.sync.get("uuid", function (obj) {
    chrome.tabs.executeScript(
        tabs[0].id,
        {code:`
        for(let a of document.querySelectorAll("#content #contents #contents a#thumbnail")){
          const xhr = new XMLHttpRequest();
          xhr.open('POST', '`+BASE_URL+`/`+obj.uuid+`/'+a.href.substring(32,43));
          xhr.send();
        }
      `});
    });
});

chrome.storage.sync.get("uuid", function (obj) {
  document.getElementById('uuidCreated').innerText = obj.uuid;
  document.querySelector("#logslink a").onclick = function () {
    chrome.tabs.create({active: true, url: BASE_URL+obj.uuid+"/logs"});
  };

  document.querySelector("#serverlinks a").onclick = function () {
    chrome.tabs.create({active: true, url: BASE_URL});
  };
});
