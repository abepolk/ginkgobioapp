function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function post (url, options) {
  const csrftoken = getCookie('csrftoken');
  const defaults = {
    'method': 'POST',
    'credentials': 'include',
    'headers': new Headers({
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'X-Requested-With': 'XMLHttpRequest'
      })
  };
  const merged = {...options, ...defaults};
  return fetch(url, merged);
}

// Next step, make sure to remove elem reporting Validation error after further POSTs

window.onload = function () {
  document.getElementById("submit").onclick = function () {
    // post needs two params as it's written
    let seq = document.getElementById("id_seq").value;
    let remove = document.getElementById("id_remove_search_history").checked;
    post("", {
      "body" : JSON.stringify({
        "seq" : seq,
        "remove_search_history" : remove
    })}).then((response) => {
      return response.json();
    }).then(data => {
      const validation_p = document.getElementById("validation_p");
      if (validation_p) {
        document.body.removeChild(validation_p);
      }
      if (data.validation_throws === 'true') {
        const para8 = document.createElement("p");
        para8.setAttribute("id", "validation_p");
        const para8_text = document.createTextNode(data.validation_error_message);
        para8.appendChild(para8_text);
        document.body.appendChild(para8);
      } else {
        const orig_result_div = document.getElementById("result_div");
          if (orig_result_div) {
            document.body.removeChild(orig_result_div);
          }
          const result_div = document.createElement("div");
          result_div.setAttribute("id", "result_div");
        if (data.result_found === 'true') {
          const len_data = data.searches.length;
          const para1 = document.createElement("p");
          // len - 1 gives most recent search, the search just made
          const para1_text = document.createTextNode("Sequence found in protein: ".concat(data.searches[len_data - 1][1]));
          para1.appendChild(para1_text);
          const para2 = document.createElement("p");
          const para2_text = document.createTextNode("Location on protein: Starts at base pair ".concat(data.searches[len_data - 1][2]));
          para2.appendChild(para2_text);
          result_div.appendChild(para1);
          result_div.appendChild(para2);
        } else {
          const para3 = document.createElement("p");
          const para3_text = document.createTextNode("Sequence not found");
          para3.appendChild(para3_text);
          result_div.appendChild(para3);
        }
        document.body.appendChild(result_div);
      }
      // Updates previous searches from JSON returned by POST
      const prev_div = document.getElementById("prev_div");
      document.body.removeChild(prev_div);
      update_searches(data.searches);
    }).catch((response) => console.log(response));
  };
  // Updates previous searches from cookie
  update_searches(searches);
};

// Returns reference to previous searches node so it can be removed later
function update_searches (searches) {
  const prev_div = document.createElement("div");
  prev_div.setAttribute("id", "prev_div");
  if (searches.length > 1) {
    const para4 = document.createElement("p");
    const para4_text = document.createTextNode("Previous searches");
    para4.appendChild(para4_text);
    prev_div.appendChild(para4);
    const len = searches.length;
    // Skip an entry if it is already displayed in result_div
    let init_index = document.getElementById("result_div") ? len - 2 : len - 1;
    // Five most recent searches excluding those in result div
    for (let i = init_index; i >= 0 && i > init_index - 5; i--) {
      let ul = document.createElement("ul");
      let li5 = document.createElement("li");
      let li5_text = document.createTextNode("Sequence: ".concat(searches[i][0]));
      li5.appendChild(li5_text);
      let li6 = document.createElement("li");
      let li6_text = document.createTextNode("Protein: ".concat(searches[i][1]));
      li6.appendChild(li6_text);
      let li7 = document.createElement("li");
      let li7_text = document.createTextNode("Location on protein: ".concat(searches[i][2]));
      li7.appendChild(li7_text);
      ul.appendChild(li5);
      ul.appendChild(li6);
      ul.appendChild(li7);
      prev_div.appendChild(ul);
    }
  }
  document.body.append(prev_div);
}
  
  